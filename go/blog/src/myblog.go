package main

import (
	"util"
	"html/template"
	// "fmt"
	"net/http"
)

func main(){
	http.HandleFunc("/", handleIndex)
	http.ListenAndServe(":8000", nil)
}

func handleIndex(w http.ResponseWriter, r *http.Request){
	t,err := template.ParseFiles("html/index.html")
	util.CheckErr(err)

	t.Execute(w, nil)
}
