package main

import (
	"database/sql"
	"fmt"
	_ "github.com/go-sql-driver/mysql"
	"os/exec"
	"strings"
	"time"
	"util"
)

type ps struct {
	Pid   string
	Cmd   string
	Start string
}

func FetchPsTask() {
	ticker := time.NewTicker(10 * time.Second)
	quit := make(chan struct{})
	go func() {
		for {
			select {
			case <-ticker.C:
				fetchPs()
			case <-quit:
				ticker.Stop()
				return
			}
		}
	}()
}

func fetchPs() {
	out, err := exec.Command("ps", "-eo", "pid,cmd,lstart").Output()
	util.CheckErr(err)
	parseAndSavePsInfo(fmt.Sprintf("%s", out))
}

func parseAndSavePsInfo(out string) {
	for _, line := range strings.Split(out, "\n")[1:] {
		tmp := strings.Split(strings.TrimSpace(line), " ")
		var strs []string
		for _, s := range tmp {
			if s != "" && s != " " {
				strs = append(strs, s)
			}
		}
		if len(strs) > 6 {
			p := new(ps)
			p.Pid = strs[0]
			p.Cmd = strings.Join(strs[1:len(strs)-5], " ")
			p.Start = strings.Join(strs[len(strs)-5:], " ")
			insertPsIntoDb(p)
		}
	}
}

var db *sql.DB
var queryStmt *sql.Stmt
var updateStmt *sql.Stmt
var insertStmt *sql.Stmt
var queryListStmt *sql.Stmt

func InitDb() {
	db, _ = sql.Open("mysql", "tiger:123456@/ps?charset=utf8")
	//检查表是否存在
	db.Exec(`
create table if not exists history(
id int auto_increment primary key,
cmd varchar(50) not null ,
start text,
unique key (cmd)
)character set utf8;`)
	queryStmt, _ = db.Prepare("select id,start from history where cmd = ?")
	updateStmt, _ = db.Prepare("update history set start = ? where id = ?")
	insertStmt, _ = db.Prepare("insert into history(cmd, start) values(?, ?)")
	queryListStmt, _ = db.Prepare("select cmd,start from history where instr(cmd, ?) > 0")
	db.SetMaxOpenConns(10)
}

func CloseDb() {
	db.Close()
}

func QueryPsList(pname string) []ps {
	var pss []ps
	rows, err := queryListStmt.Query(pname)
	util.CheckErr(err)
	defer rows.Close()
	for rows.Next() {
		p := new(ps)
		rows.Scan(&p.Cmd, &p.Start)
		p.Start = strings.Replace(p.Start, "//", "\n", -1)
		pss = append(pss, *p)
	}
	return pss
}

func contains(s []string, e string) bool {
	for _, a := range s {
		if strings.EqualFold(a, e) {
			return true
		}
	}
	return false
}

func insertPsIntoDb(p *ps) {
	// queryStr := "select id,start from history where cmd = '" + p.Cmd + "';"
	// fmt.Println(queryStr)
	rows, err := queryStmt.Query(p.Cmd)
	util.CheckErr(err)
	defer rows.Close()
	if rows.Next() {
		//如果存在cmd,检查最后一次启动时间，不一样就更新
		var id int
		var start string
		err = rows.Scan(&id, &start)
		util.CheckErr(err)
		//启动时间以“//”分隔，最多十个
		var newVal string
		starts := strings.Split(start, "//")
		if len(starts) == 0 {
			newVal = p.Start
		} else if !contains(starts, p.Start) {
			starts = append(starts, p.Start)
			if len(starts) > 10 {
				newVal = strings.Join(starts[1:], "//")
			} else {
				newVal = strings.Join(starts, "//")
			}
		} else {
			return
		}
		util.CheckErr(err)
		updateStmt.Exec(newVal, id)
	} else {
		//不存在，直接插入
		util.CheckErr(err)
		insertStmt.Exec(p.Cmd, p.Start)
	}
}
