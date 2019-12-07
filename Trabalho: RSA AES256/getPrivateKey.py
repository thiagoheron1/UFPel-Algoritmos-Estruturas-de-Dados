#!/usr/bin/env python
# coding: utf-8

# In[17]:


from Crypto.PublicKey import RSA


# In[18]:


publicKey='''-----BEGIN PUBLIC KEY-----
MEEwDQYJKoZIhvcNAQEBBQADMAAwLQImDlsTjeFVTgo4BAs9/Ex5xUU6iWNoBDY8
J7tuuv7INMmMOgYoIFUCAwEAAQ==
-----END PUBLIC KEY-----'''


# In[19]:


pubkey = RSA.importKey(publicKey)
print("N: ", pubkey.n)
print("E: ", pubkey.e)


# In[20]:


p = 1332830227949273521465367319234277279439624789
q = 1371293089587387292180481293784036793076837889
n = p*q
phi = (p-1)*(q-1)
def egcd(a, b):
    if a == 0:
        return (b, 0 , 1)
    
    g, y, x = egcd(b%a, a)
    return (g, x - (b//a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Excpetion('No modular inverse')
    return x%m

e = 65537
d = modinv(e, phi)

print("P = ", p)
print("Q = ", q)
print("N = ", n)
print("Phi = ", phi)
print("E = ", e)
print("D = ", d)
print("(E*D)%Phi = ", (e*d)%phi)


key_params = (n, e, d, p, q, phi)
private_key = RSA.construct(key_params)
pv = private_key.exportKey()
print("\n", pv)


# In[ ]:





# In[ ]:




