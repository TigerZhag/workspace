package main

import (
	"util"
	"fmt"
	"log"
	"net/http"
	"html/template"
)

func main(){
	http.HandleFunc("/", handler)
	log.Fatal(http.ListenAndServe("localhost:8000", nil))
}

func handler(w http.ResponseWriter, r *http.Request){
	// 返回html界面
	fmt.Println(r.Method)
	if r.Method == "GET" {
		//return html template
		t,err := template.ParseFiles("html/index.gtpl")
		util.CheckErr(err)

		t.Execute(w, nil)
	}else {
		r.ParseForm()
		//return result
		fmt.Println(r.Form["start"])
		fmt.Println(r.Form["end"])

		fmt.Fprint(w, "您设定的起点: %s\n您设定的终点: %s\n", r.Form["start"], r.Form["end"])
	}
}
