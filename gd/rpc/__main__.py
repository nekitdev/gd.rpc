from entrypoint import entrypoint

from gd.rpc.main import rpc

entrypoint(__name__).call(rpc)
