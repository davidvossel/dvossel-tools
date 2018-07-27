package main

import (
	"crypto"
	"crypto/rand"
	"crypto/rsa"
	"crypto/sha256"
	"crypto/x509"
	"encoding/base64"
	"fmt"
	"io/ioutil"
	"os"
)

var ciphertext []byte
var signature []byte

func writePublicKey(key *rsa.PublicKey, file string) {
	bytes := x509.MarshalPKCS1PublicKey(key)

	base64Str := base64.StdEncoding.EncodeToString(bytes)

	fmt.Println(base64Str)
	fmt.Println()
	err := ioutil.WriteFile(file, []byte(base64Str), 0600)
	if err != nil {
		fmt.Println(err.Error)
		os.Exit(1)
	}
}

func readPublicKey(file string) *rsa.PublicKey {
	bytes64, err := ioutil.ReadFile(file)

	bytes64Str := string(bytes64)
	bytes, err := base64.StdEncoding.DecodeString(bytes64Str)
	if err != nil {
		fmt.Println(err.Error)
		os.Exit(1)
	}

	key, err := x509.ParsePKCS1PublicKey(bytes)
	if err != nil {
		fmt.Println(err.Error)
		os.Exit(1)
	}
	return key

}

func writePrivateKey(key *rsa.PrivateKey, file string) {
	bytes := x509.MarshalPKCS1PrivateKey(key)

	base64Str := base64.StdEncoding.EncodeToString(bytes)

	fmt.Println(base64Str)
	fmt.Println()
	err := ioutil.WriteFile(file, []byte(base64Str), 0600)
	if err != nil {
		fmt.Println(err.Error)
		os.Exit(1)
	}
}

func readPrivateKey(file string) *rsa.PrivateKey {
	bytes64, err := ioutil.ReadFile(file)

	bytes64Str := string(bytes64)
	bytes, err := base64.StdEncoding.DecodeString(bytes64Str)
	if err != nil {
		fmt.Println(err.Error)
		os.Exit(1)
	}

	key, err := x509.ParsePKCS1PrivateKey(bytes)
	if err != nil {
		fmt.Println(err.Error)
		os.Exit(1)
	}
	return key

}

func generateKeys() {
	uploaderPrivate, err := rsa.GenerateKey(rand.Reader, 2048)
	if err != nil {
		fmt.Println(err.Error)
		os.Exit(1)
	}

	proxyPrivate, err := rsa.GenerateKey(rand.Reader, 2048)
	if err != nil {
		fmt.Println(err.Error)
		os.Exit(1)
	}

	uploaderPublic := &uploaderPrivate.PublicKey
	proxyPublic := &proxyPrivate.PublicKey

	writePublicKey(uploaderPublic, "uploaderPublic")
	writePublicKey(proxyPublic, "proxyPublic")

	writePrivateKey(uploaderPrivate, "uploaderPrivate")
	writePrivateKey(proxyPrivate, "proxyPrivate")
}

func encrypt() {
	uploaderPrivate := readPrivateKey("uploaderPrivate")
	proxyPublic := readPublicKey("proxyPublic")

	message := []byte("the code must be like a piece of music")
	label := []byte("")
	hash := sha256.New()

	var err error
	ciphertext, err = rsa.EncryptOAEP(hash, rand.Reader, proxyPublic, message, label)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	var opts rsa.PSSOptions
	opts.SaltLength = rsa.PSSSaltLengthAuto
	PSSmessage := message
	newhash := crypto.SHA256
	pssh := newhash.New()
	pssh.Write(PSSmessage)
	hashed := pssh.Sum(nil)

	signature, err = rsa.SignPSS(rand.Reader, uploaderPrivate, newhash, hashed, &opts)

	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}

func decrypt() {
	label := []byte("")
	hash := sha256.New()

	uploaderPublic := readPublicKey("uploaderPublic")
	proxyPrivate := readPrivateKey("proxyPrivate")

	// Decrypt Message
	plainText, err := rsa.DecryptOAEP(hash, rand.Reader, proxyPrivate, ciphertext, label)

	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	fmt.Printf("OAEP decrypted [%x] to \n[%s]\n", ciphertext, plainText)

	var opts rsa.PSSOptions
	opts.SaltLength = rsa.PSSSaltLengthAuto
	newhash := crypto.SHA256
	pssh := newhash.New()
	pssh.Write(plainText)
	hashed := pssh.Sum(nil)

	//Verify Signature
	err = rsa.VerifyPSS(uploaderPublic, newhash, hashed, signature, &opts)

	if err != nil {
		fmt.Println("Who are U? Verify Signature failed")
		os.Exit(1)
	} else {
		fmt.Println("Verify Signature successful")
	}
}

func main() {
	generateKeys()
	encrypt()
	decrypt()
}
