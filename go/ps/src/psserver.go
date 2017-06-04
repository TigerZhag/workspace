package main

import (
	"fmt"
	"github.com/julienschmidt/httprouter"
	"html/template"
	"log"
	"net/http"
	"time"
	"util"
)

func index(w http.ResponseWriter, r *http.Request, _ httprouter.Params) {
	//登录界面，检测cookies true=>跳转主页 false=>登录
	if r.Method == "GET" {
		temp, err := template.ParseFiles("tmpl/login.html")
		util.CheckErr(err)
		temp.Execute(w, nil)
	} else if r.Method == "POST" {
		//检测表单
		r.ParseForm()
		name := r.Form["username"][0]
		psw := r.Form["password"][0]
		if name == "zhangshixin" && psw == "123" {
			//验证通过，设置cookies，重定向到主页
			expiration := time.Now().Add(365 * 24 * time.Hour)
			cookieName := http.Cookie{Name: "username", Value: name, Expires: expiration}
			cookiePsw := http.Cookie{Name: "psw", Value: encryptString(psw), Expires: expiration}
			http.SetCookie(w, &cookieName)
			http.SetCookie(w, &cookiePsw)
			// http.Redirect(w, r, "/home", 307)
			w.Write([]byte("验证成功"))
			return
		} else {
			//密码错误，一个IP最多五次错误机会
			w.WriteHeader(http.StatusUnauthorized)
			w.Write([]byte("密码错误,请查证后再尝试"))
			return
		}
	}
}

func homepage(w http.ResponseWriter, r *http.Request, _ httprouter.Params) {
	//获取cookie，如果没有，重定向至登录界
	if !CheckCookie(r) {
		http.Redirect(w, r, "/", 307)
		w.Write([]byte("请登录"))
		return
	}
	//检索线程界面
	temp, err := template.ParseFiles("tmpl/homepage.html")
	util.CheckErr(err)
	temp.Execute(w, nil)
}

func getProcessHistory(w http.ResponseWriter, r *http.Request, _ httprouter.Params) {
	if !CheckCookie(r) {
		http.Redirect(w, r, "/", 307)
		w.Write([]byte("请登录"))
		return
	}
	r.ParseForm()
	pName := r.Form["pname"][0]
	if pName == "" {
		//
	}
	//获取进程启动信息
	fmt.Print(pName)
	tmpl, err := template.ParseFiles("tmpl/pss.html")
	util.CheckErr(err)
	tmpl.Execute(w, QueryPsList(pName))
}

func main() {
	//定时获取进程启动信息
	InitDb()
	FetchPsTask()

	router := httprouter.New()
	router.ServeFiles("/public/*filepath", http.Dir("public/"))
	router.GET("/", index)
	router.POST("/", index)
	router.GET("/home", homepage)
	router.POST("/home", getProcessHistory)
	log.Fatal(http.ListenAndServe(":8000", router))
}
