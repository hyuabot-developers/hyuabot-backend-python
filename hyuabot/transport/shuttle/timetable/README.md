![Shuttlecock Logo](./images/logo.png)

# Shuttlecock API

API to get timetable of Shuttlebus in Hanyang University ERICA

## Demo
[카카오톡 플러스친구 휴아봇](https://pf.kakao.com/_MkFlC)

## Usage

If you want to get timetable for Shuttlebus in Hanyang University ERICA, just send `GET` HTTP request to `https://raw.githubusercontent.com/jil8885/ShuttlecockAPI/master/:term/:params`

## API Documents

This phase describes about word in this API

### Bus stop

* `shuttleIn`: The bus stop at Shuttlecock to go to Hanyang University at Ansan Station or Ansan Bus Terminal
* `shuttleOut`: The bus stop at Shuttlecock coming from Hanyang University at Ansan Station or Ansan Bus Terminal
* `subway`: The bus stop at Hanyang University at Ansan Station
* `terminal`: The bus stop at Ansan Bus Terminal
* `dorm`: The bus stop at Dormitory in Hanyang University ERICA

### Bus type

* `toSubway`: The bus to go to Hanyang Univeristy at Ansan Station
* `toTerminal`: The bus to go to Ansan Bus Terminal
* `cycle`: The bus for cycle route

### Semester

For timetable during semester

###### Week

`Monday` to `Friday` on semester

```
$ curl https://raw.githubusercontent.com/jil8885/ShuttlecockAPI/master/semester/week.json
```

###### Weekend

`Saturday` or `Sunday` or `holiday` on semster

```
$ curl https://raw.githubusercontent.com/jil8885/ShuttlecockAPI/master/semester/weekend.json
```

### Seasonal semester

For timetable during seasonal vacation

###### Week

`Monday` to `Friday` on vacation

```
$ curl https://raw.githubusercontent.com/jil8885/ShuttlecockAPI/master/seasonal/week.json
```

###### Weekend

`Saturday` or `Sunday` or `holiday` on semster

```
$ curl https://raw.githubusercontent.com/jil8885/ShuttlecockAPI/master/seasonal/weekend.json
```


### Vacation

For timetable during vacation

###### Week

`Monday` to `Friday` on vacation

```
$ curl https://raw.githubusercontent.com/jil8885/ShuttlecockAPI/master/vacation/week.json
```

###### Weekend

`Saturday` or `Sunday` or `holiday` on semster

```
$ curl https://raw.githubusercontent.com/jil8885/ShuttlecockAPI/master/vacation/weekend.json
```
