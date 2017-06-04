package main

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"encoding/base64"
	"fmt"
	"io"
	"net/http"
	"util"
)

func encryptString(str string) string {
	key := []byte("tiger.zhagkeykey")
	plainText := []byte(str)
	block, err := aes.NewCipher(key)
	util.CheckErr(err)
	cipherText := make([]byte, aes.BlockSize+len(plainText))
	iv := cipherText[:aes.BlockSize]
	_, err = io.ReadFull(rand.Reader, iv)
	util.CheckErr(err)
	stream := cipher.NewCFBEncrypter(block, iv)
	stream.XORKeyStream(cipherText[aes.BlockSize:], plainText)
	return base64.URLEncoding.EncodeToString(cipherText)
}

// decrypt from base64 to decrypted string
func decrypt(cryptoText string) string {
	key := []byte("tiger.zhagkeykey")
	ciphertext, _ := base64.URLEncoding.DecodeString(cryptoText)
	block, err := aes.NewCipher(key)
	if err != nil {
		panic(err)
	}

	// The IV needs to be unique, but not secure. Therefore it's common to
	// include it at the beginning of the ciphertext.
	if len(ciphertext) < aes.BlockSize {
		panic("ciphertext too short")
	}
	iv := ciphertext[:aes.BlockSize]
	ciphertext = ciphertext[aes.BlockSize:]

	stream := cipher.NewCFBDecrypter(block, iv)

	// XORKeyStream can work in-place if the two arguments are the same.
	stream.XORKeyStream(ciphertext, ciphertext)

	return fmt.Sprintf("%s", ciphertext)
}

func CheckRawUser(name string, psw string) bool {
	return name == "zhangshixin" && psw == "123"
}

func CheckCookie(r *http.Request) bool {
	userName, err := r.Cookie("username")
	psw, err := r.Cookie("psw")
	if err != nil {
		return false
	}
	if userName.Value == "" || psw.Value == "" || userName.Value != "zhangshixin" || decrypt(psw.Value) != "123" {
		return false
	}
	return true
}
