
import os
from concurrent import futures
import grpc
import time
import chunk_pb2, chunk_pb2_grpc

CHUNK_SIZE = 1024 * 1024  # 1MB

def read_chunks(filename):    
	if (not os.path.isfile(filename) ) or ( filename == None ):
		print("file does not exist or filename is None")
		yield chunk_pb2.Content(data=None)
		return
 
	with open(filename, 'rb') as f:
		while True:
			piece = f.read(CHUNK_SIZE)
			if len(piece) == 0:
				return
			yield chunk_pb2.Content(data=piece)


def write_chunks(chunks, filename):    
    with open(filename, 'wb') as f:
        for chunk in chunks:            
            f.write(chunk.data)


class FileHanlder(chunk_pb2_grpc.FileHandlerServicer):
	
	def __init__(self):
		self.in_file = None
		self.out_file = None
		# init client stub

		
	def set(self, request, context):
		self.in_file = request.src
		self.out_file = request.dst
		
		# todo: check file is valid
		return chunk_pb2.File(src = self.in_file, dst = self.out_file, size = 0)

	def ul(self, request_iterator, context):
		print("ul src {}".format(self.in_file) )
		print("ul dst {}".format(self.out_file) )

		if self.out_file == None:
			return chunk_pb2.File(src=self.in_file, dst=self.out_file, size = -1)
						
		write_chunks(request_iterator, self.out_file)		
		size = os.path.getsize(self.out_file)
		return chunk_pb2.File(src=self.in_file, dst=self.out_file, size = size)


	def dl(self, request, context):
		
		self.in_file = request.src
		self.out_file = request.dst
				
		print("dl src {}".format(self.in_file) )
		print("dl dst {}".format(self.out_file) )

		data = read_chunks(self.in_file)
				
		return data #chunk_pb2.Content(data)
		
		    
def run_handler(port = 8888, max_workers = 1):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    chunk_pb2_grpc.add_FileHandlerServicer_to_server(FileHanlder(), server)

    server.add_insecure_port('[::]:{}'.format(port))
    server.start()

    hold()


def hold():
    try:
        while True:
            time.sleep(60*60*24)
    except KeyboardInterrupt:
        exit(0)


if __name__ == '__main__':
    #server = FileServer().start()
    run_handler(port = 8888)
    
