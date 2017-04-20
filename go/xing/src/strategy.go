package main

import (
	"time"
)

//分段
type Segment struct{
	Transportation string//交通工具
	Cost int             //费用(RMB)
	TimeConsuming time.Duration //耗时
	StartTime time.Time  //起始时间
	EndTime time.Time    //终止时间
	Outset string        //起点
	Destination string   //终点
}

//总策略
type Strategy struct{
	Segments []Segment
	Cost int
	TimeConsuming time.Duration
	StartTime time.Time
	EndTime time.Time
	Outset string
	Destination string
}
