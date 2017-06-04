package main

import (
	"fmt"
	"io"
	"log"
	"net"
	"time"
)

func main() {
	// go spinner(100 * time.Millisecond)
	// const n = 45
	// fibN := fib(n)
	// fmt.Printf("\rFibonacci(%d) = %d\n", n, fibN)

	// listener, err := net.Listen("tcp", "localhost:8000")
	// if err != nil{
	// 	log.Fatal(err)
	// }

	// for {
	// 	conn, err := listener.Accept()
	// 	if err != nil {
	// 		log.Print(err)
	// 	}
	// 	go handleConn(conn)
	// }
}

func handleConn(c net.Conn) {
	defer c.Close()
	for {
		_, err := io.WriteString(c, time.Now().Format("15:04:05\n"))
		if err != nil {
			return
		}
		time.Sleep(1 * time.Second)
	}
}

func spinner(delay time.Duration) {
	for {
		for _, r := range `-\|/` {
			fmt.Printf("\r%c", r)
			time.Sleep(delay)
		}
	}
}

func fib(x int) int {
	if x < 2 {
		return x
	}
	return fib(x-1) + fib(x-2)
}
