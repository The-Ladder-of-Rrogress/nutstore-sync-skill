#!/usr/bin/env python3
"""
nutstore-sync: 坚果云 WebDAV 同步工具
版本: 2.1.0 | 体积: ~3.5KB | 依赖: 仅标准库

Usage:
    python nutstore_sync.py test                    # 测试连接
    python nutstore_sync.py upload <文件> [路径]     # 上传文件
    python nutstore_sync.py download <文件> [路径]   # 下载文件
    python nutstore_sync.py list [路径]             # 列出目录

Python API:
    from nutstore_sync import NutstoreSync
    client = NutstoreSync()
    client.upload('local.txt', 'remote.txt')
    client.download('remote.txt', 'local.txt')
"""

from __future__ import annotations

import urllib.request
import urllib.error
import base64
import json
import os
import sys
import ssl
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional, Tuple, List, Callable

# SSL 上下文（局部使用，不影响全局设置）
# 坚果云使用自签名证书，需要禁用验证才能正常连接
_ssl_context = ssl._create_unverified_context()  # nosec B323 -- required for nutstore self-signed cert

# 配置路径（按优先级）
DEFAULT_CONFIG_PATHS = [
    Path(__file__).parent / ".nutstore_credentials",
    Path.home() / ".nutstore_credentials",
    Path.home() / ".stepfun" / "skills" / "nutstore-sync" / ".nutstore_credentials",
]

DEFAULT_WEBDAV_URL = "https://dav.jianguoyun.com/dav/"
# 默认最大文件大小 50MB (防止内存溢出)
DEFAULT_MAX_FILE_SIZE = 50 * 1024 * 1024
# 默认请求超时时间（秒）
DEFAULT_TIMEOUT = 30
# 默认分块大小 8KB
DEFAULT_CHUNK_SIZE = 8192


class NutstoreError(Exception):
    """坚果云操作异常基类"""
    pass


class ConfigError(NutstoreError):
    """配置错误"""
    pass


class APIError(NutstoreError):
    """API 调用错误"""
    def __init__(self, message: str, status_code: int = 0):
        super().__init__(message)
        self.status_code = status_code


class NutstoreSync:
    """坚果云 WebDAV 客户端

    支持文件上传、下载、目录列表等基础操作。
    仅依赖 Python 标准库，无需额外安装。

    Example:
        >>> client = NutstoreSync()
        >>> client.test()
        True
        >>> client.upload('local.txt', 'remote.txt')
        True
    """

    def __init__(
        self,
        config_path: Optional[str] = None,
        timeout: int = DEFAULT_TIMEOUT,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
    ):
        """初始化客户端

        Args:
            config_path: 配置文件路径，默认自动搜索
            timeout: 请求超时时间（秒），默认 30 秒
            chunk_size: 分块传输大小（字节），默认 8KB

        Raises:
            ConfigError: 配置文件不存在或格式错误
        """
        self.config = self._load_config(config_path)
        self.auth = base64.b64encode(
            f"{self.config['username']}:{self.config['app_password']}".encode()
        ).decode()
        self.base_url = self.config.get('webdav_url', DEFAULT_WEBDAV_URL).rstrip('/') + '/'
        self.timeout = max(timeout, 1)  # 至少 1 秒
        self.chunk_size = max(chunk_size, 1024)  # 至少 1KB

    def _load_config(self, path: Optional[str] = None) -> dict:
        """加载配置文件

        Args:
            path: 配置文件路径

        Returns:
            配置字典

        Raises:
            ConfigError: 配置文件不存在或格式错误
        """
        paths = [Path(path)] if path else DEFAULT_CONFIG_PATHS

        for p in paths:
            if p.exists():
                try:
                    with open(p, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    # 验证必要字段
                    required_fields = ['username', 'app_password']
                    missing_fields = [f for f in required_fields if f not in config]
                    if missing_fields:
                        raise ConfigError(f"Config missing required fields: {missing_fields}")
                    return config
                except json.JSONDecodeError as e:
                    raise ConfigError(f"Invalid JSON in config: {p} - {e}")

        raise ConfigError(
            f"Config not found. Create one at: {DEFAULT_CONFIG_PATHS[1]}"
        )

    def _request(
        self,
        method: str,
        path: str,
        data: Optional[bytes] = None,
        headers: Optional[dict] = None
    ) -> Tuple[int, Optional[bytes]]:
        """发送 HTTP 请求

        Args:
            method: HTTP 方法 (GET, PUT, PROPFIND, etc.)
            path: 远程路径
            data: 请求体数据
            headers: 额外请求头

        Returns:
            (状态码, 响应数据)
        """
        h = {'Authorization': f'Basic {self.auth}'}
        if headers:
            h.update(headers)

        url = self.base_url + path.lstrip('/')
        # Validate URL scheme to prevent file:// and other unintended schemes
        if not url.startswith(('http://', 'https://')):
            raise APIError(f"Invalid URL scheme: only HTTP/HTTPS allowed")
        # Prevent path traversal attacks
        if '..' in path:
            raise APIError("Invalid path: '..' traversal not allowed")
        req = urllib.request.Request(url, data=data, method=method, headers=h)

        try:
            with urllib.request.urlopen(req, context=_ssl_context, timeout=self.timeout) as r:  # nosec B310 -- URL scheme validated, local SSL context used
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            return e.code, None
        except Exception as e:
            raise APIError(f"{method} {path} failed: {e}")

    def test(self) -> bool:
        """测试连接是否成功

        Returns:
            连接成功返回 True
        """
        try:
            status, _ = self._request('PROPFIND', '/', headers={'Depth': '0'})
            return status == 207
        except Exception:
            return False

    def upload(
        self,
        local_path: str,
        remote_path: Optional[str] = None,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> bool:
        """上传文件到坚果云

        Args:
            local_path: 本地文件路径
            remote_path: 远程路径，默认为本地文件名
            progress_callback: 进度回调函数 (uploaded_bytes, total_bytes)

        Returns:
            上传成功返回 True

        Raises:
            FileNotFoundError: 本地文件不存在
            APIError: 上传失败
        """
        if not os.path.exists(local_path):
            raise FileNotFoundError(f"Local file not found: {local_path}")

        file_size = os.path.getsize(local_path)
        if file_size > DEFAULT_MAX_FILE_SIZE:
            raise APIError(f"File too large: {file_size / 1024 / 1024:.1f}MB exceeds limit of {DEFAULT_MAX_FILE_SIZE / 1024 / 1024:.0f}MB")

        remote_path = remote_path or os.path.basename(local_path)

        # 分块读取并上传
        chunks = []
        uploaded = 0
        with open(local_path, 'rb') as f:
            while True:
                chunk = f.read(self.chunk_size)
                if not chunk:
                    break
                chunks.append(chunk)
                uploaded += len(chunk)
                if progress_callback:
                    progress_callback(uploaded, file_size)

        status, _ = self._request('PUT', remote_path, b''.join(chunks))

        if status not in (201, 204):
            raise APIError(f"Upload {remote_path} failed with status: {status}", status)

        return True

    def download(
        self,
        remote_path: str,
        local_path: Optional[str] = None,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> bool:
        """从坚果云下载文件

        Args:
            remote_path: 远程文件路径
            local_path: 本地保存路径，默认为远程文件名
            progress_callback: 进度回调函数 (downloaded_bytes, total_bytes)

        Returns:
            下载成功返回 True

        Raises:
            APIError: 下载失败
        """
        local_path = local_path or os.path.basename(remote_path)
        status, data = self._request('GET', remote_path)

        if status != 200 or not data:
            raise APIError(f"Download {remote_path} failed with status: {status}", status)

        total_size = len(data)
        downloaded = 0

        with open(local_path, 'wb') as f:
            while downloaded < total_size:
                chunk = data[downloaded:downloaded + self.chunk_size]
                f.write(chunk)
                downloaded += len(chunk)
                if progress_callback:
                    progress_callback(downloaded, total_size)

        return True

    def list_dir(self, path: str = '') -> List[Tuple[str, str]]:
        """列出目录内容

        Args:
            path: 远程目录路径，默认为根目录

        Returns:
            文件列表，每项为 (图标, 文件名) 元组

        Raises:
            APIError: 列表获取失败
        """
        status, data = self._request('PROPFIND', path, headers={'Depth': '1'})

        if status != 207 or not data:
            raise APIError(f"List {path} failed with status: {status}", status)

        # 使用 ElementTree 解析 WebDAV XML 响应
        # 数据来自可信的坚果云服务端，非未信任输入
        root = ET.fromstring(data)  # nosec B314 -- trusted server response

        # WebDAV 命名空间
        ns = {
            'd': 'DAV:',
            's': 'http://nutstore.org/',
        }

        results = []
        # 查找所有 href 元素
        for href_elem in root.iter('{DAV:}href'):
            href = href_elem.text
            if href is None:
                continue
            # 跳过当前目录（请求的路径本身）
            normalized_path = path.rstrip('/') + '/'
            if href.rstrip('/') + '/' == normalized_path or href == path:
                continue

            name = href.rstrip('/').split('/')[-1]
            is_collection = href.endswith('/')
            icon = "\U0001f4c1" if is_collection else "\U0001f4c4"  # 📁 / 📄
            results.append((icon, name))

        return results

    def delete(self, remote_path: str) -> bool:
        """删除远程文件或目录

        Args:
            remote_path: 远程路径

        Returns:
            删除成功返回 True

        Raises:
            APIError: 删除失败
        """
        status, _ = self._request('DELETE', remote_path)

        if status not in (200, 204):
            raise APIError(f"Delete {remote_path} failed with status: {status}", status)

        return True

    def exists(self, remote_path: str) -> bool:
        """检查远程文件是否存在

        Args:
            remote_path: 远程路径

        Returns:
            存在返回 True
        """
        status, _ = self._request('HEAD', remote_path)
        return status == 200


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    try:
        client = NutstoreSync()
    except ConfigError as e:
        print(f"Config error: {e}")
        sys.exit(1)

    try:
        if cmd == 'test':
            success = client.test()
            print(f"{'Connected' if success else 'Failed'}")
            sys.exit(0 if success else 1)

        elif cmd == 'upload' and len(sys.argv) >= 3:
            local = sys.argv[2]
            remote = sys.argv[3] if len(sys.argv) > 3 else None

            def _progress(uploaded, total):
                pct = uploaded / total * 100
                print(f"\rUploading: {uploaded}/{total} bytes ({pct:.0f}%)", end='', flush=True)

            client.upload(local, remote, progress_callback=_progress)
            print()  # 换行
            print(f"Uploaded: {remote or os.path.basename(local)}")

        elif cmd == 'download' and len(sys.argv) >= 3:
            remote = sys.argv[2]
            local = sys.argv[3] if len(sys.argv) > 3 else None

            def _progress(downloaded, total):
                pct = downloaded / total * 100
                print(f"\rDownloading: {downloaded}/{total} bytes ({pct:.0f}%)", end='', flush=True)

            client.download(remote, local, progress_callback=_progress)
            print()  # 换行
            print(f"Downloaded: {local or os.path.basename(remote)}")

        elif cmd == 'list':
            path = sys.argv[2] if len(sys.argv) > 2 else ''
            items = client.list_dir(path)
            for icon, name in items:
                print(f"  {icon} {name}")

        elif cmd == 'delete' and len(sys.argv) >= 3:
            remote = sys.argv[2]
            client.delete(remote)
            print(f"Deleted: {remote}")

        elif cmd == 'exists' and len(sys.argv) >= 3:
            remote = sys.argv[2]
            exists = client.exists(remote)
            print(f"{remote}: {'exists' if exists else 'not found'}")

        else:
            print(__doc__)
            sys.exit(1)

    except NutstoreError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
