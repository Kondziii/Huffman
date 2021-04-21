from TreeNode import TreeNode
import heapq
import json
import socket

class Huffman:
    def __init__(self):
        self.text = None
        self.codedText = None
        self.frequencies = {}
        self.heapNodes = []
        self.coddedLetters = {}
        self.reversedCoddedLetters = {}
        self.numberZeros = 0

    def calculateFrequencies(self, pathToText):
        file = open(pathToText, 'r')
        self.text = file.read()
        file.close()
        for letter in self.text:
            if letter in self.frequencies:
                self.frequencies[letter] += 1
            else:
                self.frequencies[letter] = 0

    def buildHuffmanTree(self):
        [heapq.heappush(self.heapNodes, TreeNode(letter, self.frequencies[letter])) for letter in self.frequencies]

        while self.heapNodes.__len__() > 1:
            smallestNodes = [heapq.heappop(self.heapNodes) for i in range(2)]
            heapq.heappush(self.heapNodes, TreeNode(None, smallestNodes[0].frequency + smallestNodes[1].frequency,
                                                    smallestNodes[0], smallestNodes[1]))

    def calculateCodedLetters(self, code, node):
        if node.letter is not None:
            self.coddedLetters[node.letter] = code
            return
        self.calculateCodedLetters(code + "0", node.leftNode)
        self.calculateCodedLetters(code + "1", node.rightNode)

    def getCodedText(self):
        encodedText = ""
        for letter in self.text:
            encodedText += self.coddedLetters[letter]
        return encodedText

    def compressFile(self, pathToText, pathToCode, pathToDict):
        self.calculateFrequencies(pathToText)
        self.buildHuffmanTree()
        self.calculateCodedLetters("", heapq.heappop(self.heapNodes))
        file = open(pathToDict, 'w')
        file.write(json.dumps(self.coddedLetters, indent=2))
        file.close()
        self.codedText = self.getCodedText()
        self.numberZeros = 0
        for i in range(8 - self.codedText.__len__() % 8):
            self.codedText += '0'
            self.numberZeros += 1

        bytes = bytearray()
        for i in range(0, len(self.codedText), 8):
            byte = self.codedText[i:i + 8]
            bytes.append(int(byte, 2))
        file = open(pathToCode, 'wb')
        file.write(bytes)
        file.close()

    def decodeText(self, codedText):
        code = ""
        decodedText = ""
        for i in codedText:
            code += i
            if code in self.reversedCoddedLetters:
                decodedText += self.reversedCoddedLetters[code]
                code = ""
        return decodedText

    def decompressFile(self, pathToCode, pathToDecode, pathToDict, zeros):
        self.numberZeros = int(zeros)
        self.coddedLetters = json.loads(open(pathToDict).read().replace("}{", "},{"))
        self.reversedCoddedLetters = {value: key for (key, value) in self.coddedLetters.items()}
        with open(pathToCode, 'rb') as fileInput, open(pathToDecode, 'w') as fileOutput:
            code = ""

            byte = fileInput.read(1)
            while (len(byte) > 0):
                code += bin(ord(byte))[2:].rjust(8, '0')
                byte = fileInput.read(1)
        codedText = code[:code.__len__() - self.numberZeros]
        decodedText = self.decodeText(codedText)
        file = open(pathToDecode, 'w')
        file.write(decodedText)
        file.close()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234))
receivedMessage = ""
n = s.recv(1)
zeros = n.decode('utf-8')

while True:
    print('receiving data...')
    data = s.recv(8)
    print('data=', (data))
    if not data:
        break
    receivedMessage += data.decode("ANSI")
    print('Successfully get the file')

open('encodedText.txt', 'wb').write(bytes(receivedMessage[:receivedMessage.find('EOF')], 'ANSI'))
open('dict.txt', 'w').write(receivedMessage[receivedMessage.find('EOF')+3:].replace('\n', ""))

h = Huffman()
h.decompressFile('encodedText.txt', 'decodedText.txt', 'dict.txt', zeros)

s.close()
print('connection closed')


