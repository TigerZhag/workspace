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
	http.Handle("/public/", http.StripPrefix("/public/", http.FileServer(http.Dir("public"))))
	log.Fatal(http.ListenAndServe("localhost:8000", nil))
}

func handler(w http.ResponseWriter, r *http.Request){
	// 返回html界面
	if r.Method == "GET" {
		//return html template
		t,err := template.ParseFiles("html/index.html")
		util.CheckErr(err)

		t.Execute(w, nil)
	}else {
		r.ParseForm()
		//return result
		start := r.Form["start"][0]
		end := r.Form["end"][0]
		date := r.Form["date"][0]
		fmt.Fprintf(w, "<center>您设定的起点: %s\n您设定的终点: %s\n您设定的日期: %s\n</center>", start, end, date)

		//过滤输入

		//直达方法/费用
		s := GetDirectStrategy(start, end, date)
		fmt.Println(s.Cost)
		//铁路方法&费用(高德地图)

		//排序及推荐
	}
}

func handleResult(w http.ResponseWriter, r *http.Request){
	fmt.Println("ssssss")
	fmt.Fprint(w, "i am from route result")
}
