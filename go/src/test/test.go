package main

import (
	"fmt"
	"util"
	"database/sql"
	_ "github.com/go-sql-driver/mysql"
)

func main(){
	db, err := sql.Open("mysql", "tiger:123456@/jianshu_blog?charset=utf8mb4")
	util.CheckErr(err)

	_, err = db.Exec("create table if not exists test (id integer auto_increment primary key, title text);")
	util.CheckErr(err)

	stmt, err := db.Prepare("insert into test(title) values(?)")
	util.CheckErr(err)

	_, err = stmt.Exec("父亲的往事")
	util.CheckErr(err)

	rows, err := db.Query("select title from test;")
	for rows.Next(){
		var title string
		err = rows.Scan(&title)
		util.CheckErr(err)

		fmt.Println(title)
	}
}
