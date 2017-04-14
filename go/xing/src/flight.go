package main

import (
	"fmt"
	"util"
	"github.com/PuerkitoBio/goquery"
	iconv "github.com/djimenez/iconv-go"
	"net/http"
	"database/sql"
	_ "github.com/go-sql-driver/mysql"
)

func GetAllAirport() []string {
	res, err := http.Get("http://flights.ctrip.com/process/schedule/")
	util.CheckErr(err)
	defer res.Body.Close()

	utfBody, err := iconv.NewReader(res.Body, "gbk", "utf-8")
	util.CheckErr(err)

	doc, err := goquery.NewDocumentFromReader(utfBody)
	util.CheckErr(err)

	db, err := sql.Open("mysql", "tiger:123456@/chunlv?charset=utf8")
	util.CheckErr(err)
	defer db.Close()

	// stmt, err := db.Prepare("update airports set city = '?' where name like '?%';");
	// util.CheckErr(err)

	var result []string
	doc.Find(".letter_list li .m a").Each(func(i int, s *goquery.Selection){
		//for each item found
		r := []rune(s.Text())
		city := string(r[:len(r) - 2])
		// fmt.Printf("%s, %d\n", city, len(r))

		//验证机场名称
		str := "update airports set city = '" + city + "' where name like '" + city + "%';"
		fmt.Println(str)
		db.Exec(str)
		// stmt.Exec(city, city)

		result = append(result, s.Text())
	})
	fmt.Println(len(result))
	return result
}

// func GetAllFlight(start string) []string {
//	doc, err = goquery.NewDocument("")
// }

// 爬取所有机场信息
//
func AirportsSpyder(){
	//初始化数据库
	db, err := sql.Open("mysql", "tiger:123456@/chunlv?charset=utf8")
	util.CheckErr(err)
	defer db.Close()

	_, err = db.Exec(`
create table if not exists airports(
id int auto_increment primary key,
name varchar(20) not null,
iata varchar(5) not null,
icao varchar(5) not null,
province varchar(20) not null,
city varchar(20)
)character set utf8;`)
	util.CheckErr(err)

	stmt, err := db.Prepare("insert into airports(name, iata, icao, province) values(?,?,?,?)")
	util.CheckErr(err)

	url := "https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E6%9C%BA%E5%9C%BA%E8%BF%90%E8%90%A5%E7%BB%9F%E8%AE%A1%E5%88%97%E8%A1%A8#2016.E5.B9.B4"

	doc, err := goquery.NewDocument(url)
	util.CheckErr(err)

	doc.Find("div.mw-collapsible-content").Eq(0).Find("table tbody tr").Each(func(i int, s *goquery.Selection){
		ss := s.Find("td")
		name := ss.Eq(0).Text()
		if name == "" {
			return
		}
		iata := ss.Eq(1).Text()
		icao := ss.Eq(2).Text()
		province := ss.Eq(3).Text()

		stmt.Exec(name, iata, icao, province)
	})
}

//爬取所有城市航班联通情况
func FlightsSpyder(){

}

func fillDBCity(){

}
