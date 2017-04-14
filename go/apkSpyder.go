// author: zhang shixin
// date : 2017.3.27
package main

import (
	"fmt"
	"net/http"
	"os"
	"golang.org/x/net/html"
	"bytes"
	"io"
	"strings"
	_ "github.com/mattn/go-sqlite3"
	"database/sql"
	"log"
	"strconv"
)

func main(){
	//receive param from terminator
	//	url := "http://sj.qq.com/myapp/detail.htm?apkName=com.tencent.mm"
	for _, url := range os.Args[1:]{
		//parse html
		apkName, apkIconUrl, apkPics, apkDescribe, apkUrl := fetch(url)

		//download icon, pictures, apk
		// fmt.Println(apkName)
		// fmt.Println(apkIconUrl)
		// fmt.Println(strings.Join(apkPics, "\n"))
		// fmt.Println(apkDescribe)
		// fmt.Println(apkUrl)
		os.MkdirAll("./files/" + apkName, 0775)
		dir := "./files/" + apkName + "/"
		iconDst := dir + apkName + "_icon"
		apkDst := dir + apkName + "_apk.apk"
		downloadTo(apkIconUrl, iconDst)
		downloadTo(apkUrl, apkDst)
		picsDir := dir + "pics/"
		os.Mkdir(picsDir, 0775)
		for id,picUrl := range apkPics{
			picDst := picsDir + "pic" + strconv.Itoa(id)
			downloadTo(picUrl, picDst)
		}

		//save record to database
		os.Mkdir("./db", 0775)
		saveRecord(apkName, iconDst, picsDir, apkDescribe, apkDst)
	}
}

func fetch(url string)(string, string, []string, string, string){
	var apkName string
	var apkIconUrl string
	var buffer bytes.Buffer
	var apkDescribe string
	var apkPics []string
	var apkUrl string
	//get the html
	resp, err := http.Get(url)
	if err!= nil{
		fmt.Fprintf(os.Stderr, "fetch: %v\n", err)
		os.Exit(1)
	}
	defer resp.Body.Close()

	//parse html
	tokens := html.NewTokenizer(resp.Body)

	for {
		tt := tokens.Next()
		if tt == html.ErrorToken{
			break
		}else if tt == html.StartTagToken {
			t := tokens.Token()
			isAnchor := (t.Data == "div" || t.Data == "a")
			if isAnchor{
				for _,a := range t.Attr {
					if a.Key == "class" {
						switch a.Val{
						case "det-name-int":
							// apk name
							tt := tokens.Next()
							if tt == html.TextToken{
								apkName = bytesToString(tokens.Text())
							}
							break
						case "det-icon":
							//apk icon
							tokens.Next()
							tt := tokens.Next()
							if tt == html.SelfClosingTagToken {
								t := tokens.Token()
								isAnchor := t.Data == "img"
								if isAnchor {
									for _,src := range t.Attr {
										if src.Key == "src"{
											apkIconUrl = src.Val
										}
									}
								}
							}
							break
						case "pic-img-box":
							tokens.Next()
							tt := tokens.Next()
							if tt == html.SelfClosingTagToken {
								t := tokens.Token()
								isAnchor := t.Data == "img"
								if isAnchor {
									for _,src := range t.Attr {
										if src.Key == "id"{
											_ = src.Val
										}else if src.Key == "data-src"{
											apkPics = append(apkPics, src.Val)
										}
									}
								}
							}
						case "det-app-data-info":
							for {
								tt := tokens.Next()
								if tt == html.EndTagToken && tokens.Token().Data == "div"{
									buffer.WriteString("\n")
									break
								}
								if tt == html.TextToken{
									t := tokens.Token()
									buffer.WriteString(t.String())
								}
							}
						case "det-down-btn":
							for _, src := range t.Attr {
								if src.Key == "data-apkurl"{
									apkUrl = src.Val
								}
							}
						}
					}
				}
			}
		}
	}
	apkDescribe = strings.TrimSpace(buffer.String())
	return apkName, apkIconUrl, apkPics, apkDescribe, apkUrl
}

func downloadTo(src string, dst string)(int){
	out, err := os.Create(dst)
	if err != nil{
		fmt.Fprintf(os.Stderr, "create File: %v\n", err)
	}
	defer out.Close()

	resp, err := http.Get(src)
	if err != nil{
		fmt.Fprintf(os.Stderr, "download :%v\n", err)
		os.Exit(1)
	}
	defer resp.Body.Close()

	n, err := io.Copy(out, resp.Body)
	if err != nil{
		fmt.Fprintf(os.Stderr, "write file: %v\n", err)
	}
	return int(n)
}

func saveRecord(apkName string, iconSrc string, picDirSrc string, describe string, apkSrc string){
	db, err := sql.Open("sqlite3", "./db/apkRecord.db")
	if err != nil{
		log.Fatal(err)
	}
	createTableifNotExist(db)
	defer db.Close()

	//insert data
	sqlStmt := `insert into records(name, iconsrc, picsdirsrc, describe, apksrc) values(?, ?, ?, ?, ?)`
	stmt, err := db.Prepare(sqlStmt)
	if err != nil {panic(err)}
	defer stmt.Close()

	_, err = stmt.Exec(apkName, iconSrc, picDirSrc, describe, apkSrc)
	if err != nil {panic(err)}
}

func createTableifNotExist(db *sql.DB){
	sqlStmt := `create table if not exists records(id integer not null primary key autoincrement, name text, iconsrc text, picsdirsrc text, describe text, apksrc text)`
	_, err := db.Exec(sqlStmt)
	if err != nil {
		log.Fatal(err)
	}
}

func bytesToString(byteArray []byte)(string){
	// fmt.Printf("%s\n", byteArray)
	// n := bytes.Index(byteArray, []byte{0})
	// fmt.Println("%d", n)
	return string(byteArray)
}
