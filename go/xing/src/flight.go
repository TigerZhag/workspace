package main

import (
	"fmt"
	"util"
	"github.com/PuerkitoBio/goquery"
	iconv "github.com/djimenez/iconv-go"
	"net/http"
	"database/sql"
	_ "github.com/go-sql-driver/mysql"
	"strings"
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
	db, err := sql.Open("mysql", "tiger:123456@localhost/chunlv?charset=utf8")
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
	url := "http://flights.ctrip.com/process/schedule/"
	// doc := GetGbkDoc(url, "gbk")
	res ,err := http.Get(url)
	util.CheckErr(err)

	defer res.Body.Close()
	utfBody, err := iconv.NewReader(res.Body, "gbk", "utf-8")
	util.CheckErr(err)

	doc, err := goquery.NewDocumentFromReader(utfBody)
	util.CheckErr(err)

	//初始化数据库
	db,err := sql.Open("mysql", "tiger:123456@/chunlv?charset=utf8")
	util.CheckErr(err)
	defer db.Close()

	//创建数据表
	db.Exec(`
create table if not exists flights(
id int auto_increment primary key,
start int,
end int,
foreign key(start) references airports(id) on delete cascade,
foreign key(end) references airports(id) on delete cascade
)engine = innodb;
`)

	doc.Find("div.mod_box div.natinal_m ul.letter_list li").Each(func(i int, s *goquery.Selection){
		s.Find("div.m a").Each(func(i int, s *goquery.Selection){
			fmt.Println(s.Text())
			cUrl, _ := s.Attr("href")
			if cUrl != "" {
				FlightsOfCity("http://flights.ctrip.com" + cUrl, db)
			}
		})
	})
	fmt.Println("lxxx")
}

//从url中获取该城市所有航班
func FlightsOfCity(url string, db *sql.DB){
	fmt.Println(url)
	// doc := GetGbkDoc(url, "gb2312")
	res ,err := http.Get(url)
	util.CheckErr(err)

	defer res.Body.Close()
	utfBody, err := iconv.NewReader(res.Body, "gb2312", "utf-8")

	doc, err := goquery.NewDocumentFromReader(utfBody)
	if err != nil{
		return
	}
	s := doc.Find("div.city_m div.tab_m div.item_box")
	ss := s.Find("ul.letter_list").Eq(0).Find("li")
	ss.Each(func(i int, s *goquery.Selection){
		s.Find("div.m a").Each(func(i int, s *goquery.Selection){
			//通过 阿尔山-北京 找到id插入
			flights := strings.Split(s.Text(), "-")
			fmt.Printf("起点: %s  --  终点: %s\n", flights[0], flights[1])
			db.Exec("insert into flights(start, end) select a.id,b.id from airports as a inner join(select id,city from airports) b on a.city = '" + flights[0] + "' and b.city = '" + flights[1] + "';")
			// _, err := stmt.Exec(flights[0], flights[1])
		})
	})
}

func GetGbkDoc(url string, charset string) *goquery.Document{
	res ,err := http.Get(url)
	util.CheckErr(err)

	fmt.Println("GetGbkDoc")
	defer res.Body.Close()
	utfBody, err := iconv.NewReader(res.Body, charset, "utf-8")
	util.CheckErr(err)

	doc, err := goquery.NewDocumentFromReader(utfBody)
	util.CheckErr(err)

	fmt.Println("GetGbkDoc")
	return doc
}

func fillDBCity(){

}

func GetAllTransfer(start string, end string) []Strategy {
	sqlStr := "select a.id,a.name, b.id, b.name, c.id, c.name from airports as a inner join (select id, name from airports) b inner join (select id, name from airports) c inner join (select start, end from flights where start in (select id from airports where city like '" + start + "%')) d inner join (select start, end from flights where end in (select id from airports where city like '" + end + "%')) e on a.id = d.start and b.id = d.end and c.id = e.end and d.end = e.start;"
	// sqlStr := fmt.Sprintf(str, start, end);
	fmt.Println(sqlStr)
	db, err := sql.Open("mysql", "tiger:123456@/chunlv?charset=utf8")
	rows, err := db.Query(sqlStr)

	var results []Strategy

	util.CheckErr(err)
	for rows.Next(){
		// var segments []Segment
		var sid int
		var mid int
		var eid int
		var scity string
		var mcity string
		var ecity string

		err := rows.Scan(&sid, &scity, &mid, &mcity, &eid, &ecity)
		util.CheckErr(err)

		fmt.Printf("%s--%s--%s\n", scity, mcity, ecity)
	}

	return results
}
