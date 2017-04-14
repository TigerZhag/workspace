package db

import(
	"database/sql"
	_ "github.com/go-sql-driver/mysql"
)

type PostBean struct{
	ID int
	Title string
	Author string
	Publish string
	Isdeleted int
	Content text
	Visitcount int
}

func initDb(){
	db, err := sql.Open("mysql", "tiger:123456@/jianshu_blog")
	if err != nil {
		panic(err.Error())
	}
	err = db.Ping()
	if err != nil {
		panic(err.Error())
	}
	return db
}

func QueryPosts(db sql.DB){
	mu.lock()

	mu.unlock()
}

func checkErr(err ){

}
