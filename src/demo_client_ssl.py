
import os
from concurrent import futures

import grpc
import time

import chunk_pb2 as pb2
import chunk_pb2_grpc as pb2_grpc

CHUNK_SIZE = 1024 * 1024  # 1MB

def read_chunks(filename):    
	if (not os.path.isfile(filename) ) or ( filename == None ):
		print("file does not exist or filename is None")
		yield pb2.Content(data=None)
		return
 
	with open(filename, 'rb') as f:
		while True:
			piece = f.read(CHUNK_SIZE)
			if len(piece) == 0:
				return
			yield pb2.Content(data=piece)


def write_chunks(chunks, filename):    
    with open(filename, 'wb') as f:
        for chunk in chunks:            
            f.write(chunk.data)
                  

if __name__ == '__main__':

    node_addr = 'localhost:8888'
    ca_cert = 'cert.pem'
    with open(ca_cert, 'rb') as f:
        trusted_certs = f.read()

    

    channel = None
    #channel = grpc.insecure_channel(node_addr)
    #channel = grpc.secure_channel(node_addr, credentials)
    #stub = pb2_grpc.FileHandlerStub(channel)

    try:
        credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
        channel = grpc.secure_channel(node_addr, credentials)
        stub = pb2_grpc.FileHandlerStub(channel)
    except Exception as e:
        print("?? type:")
        print(type(e))

        
    #except InactiveRpcError as e:
    #    print(e)
    
    """
        
    #ul
    in_file_name = './up_in_1.txt'
    out_file_name = './up_out_1.txt'    
    response = stub.set(pb2.File(
        src = in_file_name,
        dst = out_file_name ))

    chunks = read_chunks(in_file_name)
    
    response = stub.ul(chunks)
    print("response file size {}".format(response.size) )
    

    #dl    
    in_file_name = './dl_file_in-1.txt'
    out_file_name = './dl_file_out-1.txt'
      
    content = stub.dl(pb2.File(
        src = in_file_name,
        dst = out_file_name))

    if os.path.isfile(out_file_name):
        os.remove(out_file_name)

    write_chunks(content, out_file_name)
    """
    
    

    
        
        