package main

import (
	"util"
	"html/template"
	// "fmt"
	"net/http"
	"github.com/julienschmidt/httprouter"
	"log"
)

func Index(w http.ResponseWriter, r *http.Request, _ httprouter.Params){
	t, err := template.ParseFiles("html/index.html")
	util.CheckErr(err)
	t.Execute(w, nil)
}

func main(){
	router := httprouter.New()
	router.GET("/", Index)
	router.ServeFiles("/public/*filepath", http.Dir("public/"))
	log.Fatal(http.ListenAndServe(":8000", router))
}
