package main

import (
	"fmt"
	"util"
	"database/sql"
	_ "github.com/go-sql-driver/mysql"
)

func main(){
	db, err := sql.Open("mysql", "tiger:123456@/jianshu_blog?charset=utf8")
	util.CheckErr(err)
	defer db.Close()

	_, err = db.Exec("create table if not exists test (id integer auto_increment primary key, title text);")
	util.CheckErr(err)

	stmt, err := db.Prepare("insert into test(title) values(?)")
	util.CheckErr(err)

	str := "父亲的往事"
	_, err = stmt.Exec(str)
	fmt.Printf("%d \n%x \n%s\n", len(str), str, str)
	util.CheckErr(err)

	rows, err := db.Query("select title from test;")
	for rows.Next(){
		var title string
		err = rows.Scan(&title)
		util.CheckErr(err)

		fmt.Printf("%s \n", title)
	}
}
