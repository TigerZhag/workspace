package main

import (
	"time"
)

type Strategy struct{
	Transportation string//交通工具
	Cost int             //费用(RMB)
	TimeConsuming time.Duration //耗时
	StartTime time.Time  //起始时间
	EndTime time.Time    //终止时间
	Outset string        //起点
	Destination string   //终点
}
