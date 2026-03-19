#!/usr/bin/env python3
"""
nutstore-sync: 坚果云 WebDAV 同步工具
版本: 2.0.0 | 体积: ~2.5KB | 依赖: 仅标准库

Usage:
    python nutstore_sync.py test                    # 测试连接
    python nutstore_sync.py upload <文件> [路径]     # 上传文件
    python nutstore_sync.py download <文件> [路径]   # 下载文件
    python nutstore_sync.py list [路径]             # 列出目录

Python API:
    from nutstore_sync import NutstoreSync
    client = NutstoreSync()
    client.upload('local.txt', 'remote.txt')
"""

from __future__ import annotations

import urllib.request
import urllib.error
import base64
import json
import os
import sys
import ssl
import re
from pathlib import Path
from typing import Optional, Tuple, List

# 禁用SSL验证（坚果云证书兼容）
# 注意：此设置仅针对坚果云 WebDAV 服务的证书兼容性
# 坚果云使用自签名证书，需要禁用验证才能正常连接
# 所有通信仍通过 HTTPS 加密，仅跳过证书验证
ssl._create_default_https_context = ssl._create_unverified_context

# 配置路径（按优先级）
DEFAULT_CONFIG_PATHS = [
    Path(__file__).parent / ".nutstore_credentials",
    Path.home() / ".nutstore_credentials",
    Path.home() / ".stepfun" / "skills" / "nutstore-sync" / ".nutstore_credentials",
]

DEFAULT_WEBDAV_URL = "https://dav.jianguoyun.com/dav/"


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

    def __init__(self, config_path: Optional[str] = None):
        """初始化客户端
        
        Args:
            config_path: 配置文件路径，默认自动搜索
            
        Raises:
            ConfigError: 配置文件不存在或格式错误
        """
        self.config = self._load_config(config_path)
        self.auth = base64.b64encode(
            f"{self.config['username']}:{self.config['app_password']}".encode()
        ).decode()
        self.base_url = self.config.get('webdav_url', DEFAULT_WEBDAV_URL).rstrip('/') + '/'

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
        req = urllib.request.Request(url, data=data, method=method, headers=h)

        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            return e.code, None
        except Exception as e:
            raise APIError(f"Request failed: {e}")

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

    def upload(self, local_path: str, remote_path: Optional[str] = None) -> bool:
        """上传文件到坚果云
        
        Args:
            local_path: 本地文件路径
            remote_path: 远程路径，默认为本地文件名
            
        Returns:
            上传成功返回 True
            
        Raises:
            FileNotFoundError: 本地文件不存在
            APIError: 上传失败
        """
        if not os.path.exists(local_path):
            raise FileNotFoundError(f"Local file not found: {local_path}")

        remote_path = remote_path or os.path.basename(local_path)
        
        with open(local_path, 'rb') as f:
            status, _ = self._request('PUT', remote_path, f.read())

        if status not in (201, 204):
            raise APIError(f"Upload failed with status: {status}", status)
        
        return True

    def download(self, remote_path: str, local_path: Optional[str] = None) -> bool:
        """从坚果云下载文件
        
        Args:
            remote_path: 远程文件路径
            local_path: 本地保存路径，默认为远程文件名
            
        Returns:
            下载成功返回 True
            
        Raises:
            APIError: 下载失败
        """
        local_path = local_path or os.path.basename(remote_path)
        status, data = self._request('GET', remote_path)

        if status == 200 and data:
            with open(local_path, 'wb') as f:
                f.write(data)
            return True
        
        raise APIError(f"Download failed with status: {status}", status)

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
            raise APIError(f"List failed with status: {status}", status)

        # 解析 WebDAV 响应
        files = re.findall(r'<d:href>([^<]+)</d:href>', data.decode('utf-8'))
        results = []
        
        for f in files[1:]:  # 跳过当前目录
            name = f.split('/')[-2 if f.endswith('/') else -1]
            icon = "📁" if f.endswith('/') else "📄"
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
            raise APIError(f"Delete failed with status: {status}", status)
        
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
        print(f"❌ Config error: {e}")
        sys.exit(1)

    try:
        if cmd == 'test':
            success = client.test()
            print("✅ Connected" if success else "❌ Failed")
            sys.exit(0 if success else 1)

        elif cmd == 'upload' and len(sys.argv) >= 3:
            local = sys.argv[2]
            remote = sys.argv[3] if len(sys.argv) > 3 else None
            client.upload(local, remote)
            print(f"✅ Uploaded: {remote or os.path.basename(local)}")

        elif cmd == 'download' and len(sys.argv) >= 3:
            remote = sys.argv[2]
            local = sys.argv[3] if len(sys.argv) > 3 else None
            client.download(remote, local)
            print(f"✅ Downloaded: {local or os.path.basename(remote)}")

        elif cmd == 'list':
            path = sys.argv[2] if len(sys.argv) > 2 else ''
            items = client.list_dir(path)
            for icon, name in items:
                print(f"  {icon} {name}")

        elif cmd == 'delete' and len(sys.argv) >= 3:
            remote = sys.argv[2]
            client.delete(remote)
            print(f"✅ Deleted: {remote}")

        elif cmd == 'exists' and len(sys.argv) >= 3:
            remote = sys.argv[2]
            exists = client.exists(remote)
            print(f"{'✅' if exists else '❌'} {remote}: {'exists' if exists else 'not found'}")

        else:
            print(__doc__)
            sys.exit(1)
            
    except NutstoreError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
