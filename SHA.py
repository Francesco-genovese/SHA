import os

def file():
    while True:
        file_path = input("Inserisci il percorso completo del file di testo: ")
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                content_array = file.readlines()
            print("Contenuto del file memorizzato nell'array:")
            for line in content_array:
                print(line.strip()) 
            return content_array
            break
        else:
            print("Il file specificato non esiste.")
def data():
    f = open("output.txt", "w") 
    f.write("testo_originale: " + testo_da_hash)
    f.write("\n HASH SHA-256: " + hash_calcolato)
    f.close()

def rotazione_dorsale(x, n):
    return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF

def padding_messaggio(messaggio):
    lunghezza_originale_bits = len(messaggio) * 8
    messaggio += b'\x80'
    messaggio += b'\x00' * ((56 - len(messaggio) % 64) % 64)
    messaggio += lunghezza_originale_bits.to_bytes(8, byteorder='big')
    return messaggio

def divide_blocchi(messaggio):
    blocchi = [messaggio[i:i + 64] for i in range(0, len(messaggio), 64)]
    return blocchi

def inizializza_variabili():
    h0 = 0x6a09e667
    h1 = 0xbb67ae85
    h2 = 0x3c6ef372
    h3 = 0xa54ff53a
    h4 = 0x510e527f
    h5 = 0x9b05688c
    h6 = 0x1f83d9ab
    h7 = 0x5be0cd19
    return h0, h1, h2, h3, h4, h5, h6, h7

def sha256(messaggio):
    k = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
    ]
    h0, h1, h2, h3, h4, h5, h6, h7 = inizializza_variabili()
    messaggio = padding_messaggio(messaggio)
    blocchi = divide_blocchi(messaggio)

    for blocco in blocchi:
        parole = [int.from_bytes(blocco[i:i + 4], byteorder='big') for i in range(0, 64, 4)]

        for i in range(16, 64):
            s0 = (rotazione_dorsale(parole[i - 15], 7) ^ rotazione_dorsale(parole[i - 15], 18) ^ (parole[i - 15] >> 3))
            s1 = (rotazione_dorsale(parole[i - 2], 17) ^ rotazione_dorsale(parole[i - 2], 19) ^ (parole[i - 2] >> 10))
            parole.append((parole[i - 16] + s0 + parole[i - 7] + s1) & 0xFFFFFFFF)

        a, b, c, d, e, f, g, h = h0, h1, h2, h3, h4, h5, h6, h7

        for i in range(64):
            s0 = (rotazione_dorsale(a, 2) ^ rotazione_dorsale(a, 13) ^ rotazione_dorsale(a, 22))
            maj = (a & b) ^ (a & c) ^ (b & c)
            t2 = (s0 + maj) & 0xFFFFFFFF

            s1 = (rotazione_dorsale(e, 6) ^ rotazione_dorsale(e, 11) ^ rotazione_dorsale(e, 25))
            ch = (e & f) ^ ((~e) & g)
            t1 = (h + s1 + ch + k[i] + parole[i]) & 0xFFFFFFFF

            h = g
            g = f
            f = e
            e = (d + t1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (t1 + t2) & 0xFFFFFFFF

        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF
        h4 = (h4 + e) & 0xFFFFFFFF
        h5 = (h5 + f) & 0xFFFFFFFF
        h6 = (h6 + g) & 0xFFFFFFFF
        h7 = (h7 + h) & 0xFFFFFFFF

    hash_result = f"{h0:08x}{h1:08x}{h2:08x}{h3:08x}{h4:08x}{h5:08x}{h6:08x}{h7:08x}"
    return hash_result

# Esempio di utilizzo

while True:
    ds = input ("come vuoi criptare SHA ? da file o testo: (f / t): ")
    if(ds == 'f' or ds == 'F'):
        testo_da_hash = ' '.join(file())  
        hash_calcolato = sha256(testo_da_hash.encode('utf-8')) 
        print("Hash SHA-256:", hash_calcolato)
        data()
        break
    elif(ds == 't' or ds == 'T'):
        testo_da_hash = input ("inserisci il testo: ")
        hash_calcolato = sha256(testo_da_hash.encode('utf-8')) 
        print("Hash SHA-256:", hash_calcolato)
        data()
        break
    else:
        print("scelta non valida")

#R3tr0
#v 2.2
