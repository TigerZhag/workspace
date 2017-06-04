package main

import (
	"database/sql"
	"fmt"
	_ "github.com/go-sql-driver/mysql"
	"util"
)

type ps struct {
	cmd   string
	start string
}

func main() {
	db, err := sql.Open("mysql", "tiger:123456@/ps?charset=utf8")
	util.CheckErr(err)
	defer db.Close()
	rows, err := db.Query("select cmd,start from history where cmd like '%init%';")
	util.CheckErr(err)
	var pss []ps
	for rows.Next() {
		p := new(ps)
		rows.Scan(&p.cmd, &p.start)
		pss = append(pss, p)
	}

}
