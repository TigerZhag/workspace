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
	http.HandleFunc("/result", handleResult)
	log.Fatal(http.ListenAndServe("localhost:8000", nil))
}

func handler(w http.ResponseWriter, r *http.Request){
	// 返回html界面
	fmt.Println(r.Method)
	if r.Method == "GET" {
		//return html template
		t,err := template.ParseFiles("html/index.html")
		util.CheckErr(err)

		t.Execute(w, nil)
	}else {
		r.ParseForm()
		//return result
		fmt.Println(r.Form["start"])
		fmt.Println(r.Form["end"])

		fmt.Fprintf(w, "您设定的起点: %s\n您设定的终点: %s\n", r.Form["start"], r.Form["end"])

		//过滤输入

		//直达方法/费用

		//铁路方法&费用(高德地图)

		//排序及推荐
	}
}

func handleResult(w http.ResponseWriter, r *http.Request){
	fmt.Println("ssssss")
	fmt.Fprint(w, "i am from route result")
}
