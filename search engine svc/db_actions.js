const DBSOURCE = "data/crawled_web.db";
let sqlite3 = require('sqlite3').verbose();
let db = new sqlite3.Database(DBSOURCE);

let GetData = function (queryString, retFunc) {
    let sql =  "select m.url, m.tag, m.title, s.song, (select count(distinct ID) from songs where song like '%' || ? || '%') as count";
				sql+= " from movies as m";
				sql+= " inner join songs as s on s.id = m.id and s.song like '%' || ? || '%'";
				sql+= " where m.ID in(select distinct ID from songs where song like '%' || ? || '%')";
				sql+= " order by m.url";
				sql+= " LIMIT 100";
    let params = [queryString, queryString, queryString];
    db.all(sql, params, (err, rows) => {
        if (err) {
            retFunc([{ "error": err.message }]);
        }
        retFunc(rows);
    });
}

let GetAutoData = function(queryString, retFunc){
	let sql =  "select distinct song";
				sql+= " from songs";
				sql+= " where song like ? || '%'";
				sql+= " order by song";
				sql+= " LIMIT 5";
    let params = [queryString];
    db.all(sql, params, (err, rows) => {
        if (err) {
            retFunc([{ "error": err.message }]);
        }
        retFunc(rows);
    });
}

module.exports.GetData = GetData;
module.exports.GetAutoData = GetAutoData;