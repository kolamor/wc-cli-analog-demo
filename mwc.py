import argparse
import sys

def main():
	try:
		parser = ArgPars()
		args = parser.parse_args()
		count = Count()
		if 'f_stdin' in args:
			if len(sys.argv[1:]) == 1:
				StdinFile(parser, count)
			else:
				StdinF(parser, count)

		if 'file' in args:
			FilePossition(parser, count)
			args.file.close()
		print('')
	except KeyboardInterrupt:
		print('-h or --help')


class FlBase():
	"""Base Class """
	def __init__(self, parser, count):
		self._count	= count
		self.args_pars = parser.parse_args()
		self._file = self.get_file()
		if self.args_pars.l:
			self._rows()
		if self.args_pars.w:
			self._words()
		if self.args_pars.c:
			self._bytes()
		
		if (self.args_pars.l is False and self.args_pars.w is False 
					and self.args_pars.c is False) :
			self._get_all()
		return self


	def get_file(self):
		pass


	def _rows(self):
		self._file = self.get_file()
		rows = self._count.row_count(self._file)
		OutputResult.output_rows(rows)

	def _words(self):
		self._file = self.get_file()
		words = self._count.word_count(self._file)
		OutputResult.output_words(words)

	def _bytes(self):
		self._file = self.get_file()
		byte = self._count.byte_count(self._file)
		OutputResult.output_bytes(byte)

	def _get_all(self):
		self._rows()
		self._words()
		self._bytes()



class FilePossition(FlBase):

	def __init__(self, parser, count):
		super().__init__(parser, count)


	def get_file(self):
		parser = ArgPars()
		args_pars = parser.parse_args()
		file = args_pars.file
		return file



class StdinFile(FlBase):
	"""для одного элемента """
	def __init__(self, parser, count):
		super().__init__(parser, count)
		

	def get_file(self):
		parser = ArgPars()
		args_pars = parser.parse_args()
		file = args_pars.f_stdin
		return file


class StdinF(FlBase):
	"""для нескольких элементов """
	def __init__(self, parser, count):
		super().__init__(parser, count)

	def get_file(self):
		parser = ArgPars()
		if '_file' not in self.__dict__:
			args_pars = parser.parse_args()
			file = args_pars.f_stdin.read()
			return file		
		return self._file

	
class ArgPars(argparse.ArgumentParser):
	"""docstring for ArgPars"""
	def __init__(self):
		super().__init__()
		self.add_argument('-l', action='store_true', help="Кол-во строк")
		self.add_argument('-w', action='store_true', help="Кол-во слов")
		self.add_argument('-c', action='store_true', help="Кол-во байт")
		self._init_stdin_file()

	def _init_stdin_file(self):
		argst = sys.argv[1:]

		if '-l' in argst:
			argst.remove('-l')
		if '-w' in argst:
			argst.remove('-w')
		if '-c' in argst:
			argst.remove('-c')
		if len(argst) >= 1:
			self.add_argument('file', type=argparse.FileType('r'), help="file entry",
			 default=sys.stdin)	
		else:
			self.add_argument('-f_stdin', type=argparse.FileType('r'),
						help="file ent,", default='-')
		return self


class Count():
	"""docstring for Count"""
	def row_count(self, file):
		if isinstance(file , str):
			rows = sum(n.count('\n') for n in file)	
		else:
			rows = sum(chunk.count('\n') for chunk in file.read())
		return rows

	def byte_count(self, file):
		if isinstance(file , str):
			byte = len(file.encode())
		else:
			byte = len(file.read().encode())
		return byte

	def word_count(self, file):
		if isinstance(file , str):
			words = sum(len(chunk.split()) for chunk in file.split())
		else:
			words = sum(len(chunk.split()) for chunk in file.read().split())
		return words

		
class OutputResult():
	
	def output_rows(rows):
		print('Строк:', rows, end='   ')

	def output_words(words):
		print('Слов:', words, end='   ')

	def output_bytes(byte):
		print('Байт:', byte, end='   ')	



if __name__ == '__main__':
	main()