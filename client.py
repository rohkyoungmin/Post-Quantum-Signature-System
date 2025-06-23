import socket
import hashlib
import secrets

def send(message, signature):
    print("메시지 {} 와 Lamport 서명값 전송 완료!!".format(message))

#16진수 문자를 4비트 2진수로 변환
def char2bin(c):
    return '{:04b}'.format(int(c, 16))

def hash(str):
    return hashlib.sha256(str.encode()).hexdigest()

def zero_padding(str):
    if len(str)>=256:
        return str
    else:
        padded_str = ""
        padding_needed = 64 - len(str)
        for i in range(padding_needed):
            padded_str+='0'
        padded_str = padded_str + str
        return padded_str

#256bit에 대한 개인key 생성
def generate_private_key():
    #2x256 2차원 배열 생성
    private_key = [[0 for j in range(256)] for i in range(2)]
    for i in range(0,2):
        for j in range(0, 256):
            # 32바이트(256비트) 길이의 무작위 난수 생성
            random_bytes = secrets.token_bytes(32)
            # 생성된 난수를 16진수로 변환
            private_key[i][j] = random_bytes.hex() #256비트 랜덤값
    return private_key

#공개 key 생성
def generate_public_key(private_key):
    public_key = [[0 for j in range(256)] for i in range(2)]
    for i in range(2):
        for j in range(256):
            public_key[i][j] = hash(private_key[i][j])
    return public_key

#램포트 서명 생성 함수
def generate_signature(message, private_key):
    signature = []
    message_hash_value = zero_padding(hash(message)) #16진수 문자열, 길이:64
    print(private_key[0][255])
    print(message_hash_value)
    for i in range(len(message_hash_value)): 
        bin_value = char2bin(message_hash_value[i]) #4bit 2진수 문자열로
        for j in range(len(bin_value)):
            if bin_value[j] == '0': #메시지의 비트 값이 0일 경우
                signature.append(private_key[0][i*4+j])
            else: #메시지의 비트 값이 1일 경우
                signature.append(private_key[1][i*4+j])
    return signature

def verify_signature(message, signature, public_key):
   verified = 1
   chosen_public_key = []
   hashed_signature = []

   #메시지 해시 값 구하기
   message_hash = zero_padding(hash(message)) #길이 : 64
   
   #메시지의 해시값 각 비트에 해당하는 공개 key값 고르기
   for i in range(len(message_hash)):
      bin_value = char2bin(message_hash[i])
      for j in range(len(bin_value)):
         if bin_value[j] == '0':
            chosen_public_key.append(public_key[0][i*4+j])
         else:
            chosen_public_key.append(public_key[1][i*4+j])

   #서명자가 보낸 서명값들에 대한 hash값 구하기
   for i in range(len(signature)):
      hashed_signature.append(hash(signature[i]))

   #선택한 공개key값들과, 전달받은 서명의 hash값들을 비교하기
   for i in range(len(hashed_signature)):
      if chosen_public_key[i] != hashed_signature[i]:
         verified = 0
         break
   return verified


private_key = generate_private_key()
public_key = generate_public_key(private_key)

# 서버의 주소입니다. hostname 또는 ip address를 사용할 수 있습니다.
HOST = '127.0.0.1'  
# 서버에서 지정해 놓은 포트 번호입니다. 
PORT = 9999       


# 소켓 객체를 생성합니다. 
# 주소 체계(address family)로 IPv4, 소켓 타입으로 TCP 사용합니다.  
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# 지정한 HOST와 PORT를 사용하여 서버에 접속합니다. 
client_socket.connect((HOST, PORT))

# 메시지를 전송합니다.
message = input("enter your message: ")
client_socket.sendall(message.encode())

# 메시지를 수신합니다. 
data = client_socket.recv(1024)
print('Received', repr(data.decode()))

lamport_signature = generate_signature(message, private_key)

send(message, lamport_signature)
print("===========================================verifying...===========================================")

verification = verify_signature(message, lamport_signature, public_key)

if verification == 1:
     print("message verified!!")
else:
     print("verification failed!!")


class MerkleNode:
    def __init__(self, value):
        self.value = value
        self.hash = self.calculate_hash()
        self.left = None
        self.right = None

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(str(self.value).encode('utf-8'))
        return sha.hexdigest()


class MerkleTree:
    def __init__(self, leaf_values):
        # leaf_nodes라는 리스트를 생성합니다. 리스트 컴프리헨션을 사용하여 leaf_values 리스트의 각 값에 대해 MerkleNode 객체를 생성하고 리스트에 추가
        self.leaf_nodes = [MerkleNode(value) for value in leaf_values]

        # build_tree 메서드를 호출하여 leaf_nodes 리스트를 인자로 전달하여 Merkle Tree의 구조를 생성 >> 최종적으로 루트 노드를 반환
        self.root = self.build_tree(self.leaf_nodes)

    # build_tree : Merkle Tree의 구조를 재귀적으로 생성하는 역할
    # 인자로 현재의 level을 나타내는 리스트인 nodes가 전달
    def build_tree(self, nodes):

        # leaf node의 개수가 홀수인 경우 그대로 반환
        if len(nodes) == 1:
            return nodes[0]
        
        # 짝수인 경우, parent_nodes라는 빈 리스트를 생성
        parent_nodes = []

        # for 루프를 통해 현재 레벨의 노드들을 순회 
        # 현재 레벨의 노드들을 짝지어서 처리하기 위해 2씩 증가하는 인덱스를 생성
        # 우리는 leaf node가 512 고정이니까 len(nodes) = 512부터 시작
        for i in range(0, len(nodes), 2):
            left_node = nodes[i]
            right_node = nodes[i+1] if i+1 < len(nodes) else left_node

            # left_node와 right_node를 이용하여 create_parent_node 메서드를 호출하여 부모 노드를 생성하고, 생성된 부모 노드를 parent_nodes 리스트에 추가
            parent_node = self.create_parent_node(left_node, right_node)
            parent_nodes.append(parent_node)
        
        # 모든 반복이 완료되면 build_tree 메서드를 재귀적으로 호출하여 parent_nodes 리스트를 다음 레벨의 노드 리스트로 전달
        return self.build_tree(parent_nodes)
        # 마지막으로, 구성된 트리의 루트 노드가 반환

    def create_parent_node(self, left_node, right_node):
        parent_node = MerkleNode(left_node.value + right_node.value) #문자열 결합
        parent_node.left = left_node
        parent_node.right = right_node
        parent_node.hash = self.calculate_hash(parent_node)
        return parent_node

    def calculate_hash(self, node):
        sha = hashlib.sha256()
        sha.update((node.left.hash + node.right.hash).encode('utf-8'))
        return sha.hexdigest()


# 임의로 생성된 값으로 Merkle Tree 생성 >> leaf node 512개 무작위 생성
# leaf_values = [str(i) for i in range(512)]

leaf_values = []
for i in range(512):
    leaf_values.append(public_key)

# 차례대로 leaf node의 value값을 merkleTree 함수에 집어넣음
merkle_tree = MerkleTree(leaf_values)

print("Root Hash:", merkle_tree.root.hash)


# 소켓을 닫습니다.
client_socket.close()