package main

import (
	"fmt"
	"log"
	"net/http"
	"database/sql"
	_ "github.com/go-sql-driver/mysql"
	// "encoding/json"
	_ "unicode/utf8"
)

func main(){
	http.HandleFunc("/hotposts", handler)
	http.HandleFunc("/", handlerIndex)
	log.Fatal(http.ListenAndServe("localhost:8000", nil))
}

func handler(w http.ResponseWriter, r *http.Request){
	db, err := sql.Open("mysql", "tiger:123456@/jianshu_blog?charset=utf8mb4")
	checkErr(err)

	rows, err := db.Query("select id,title from posts limit 1")
	checkErr(err)

	for rows.Next(){
		var id int
		var title string
		rows.Scan(&id, &title)
		// utf8title,_ := utf8.DecodeRuneInString(title)
		// runes,size := utf8.DecodeRuneInString(title)
		fmt.Fprintf(w, "id : %d title: %x, \ntitle length: %d\n", id, title, len(title))
	}
}

func handlerIndex(w http.ResponseWriter, r *http.Request){
	fmt.Fprintf(w, "welcome to tiger.com")
}

func handler404(w http.ResponseWriter, r *http.Request){
	fmt.Fprintf(w, "tiger domine \n <b>404</b>\n Page not found")
}

func checkErr(err error){
	if err != nil {
		panic(err)
	}
}
