const {Client} = require
console.log('hello');

const client = new Client({
    user: 'postgres',
    host: '127.0.0.1',
    database: 'socialmedia',
    password: '060489a+',
    port: 5432,
});


client.connect((err)=>{
    if (err){
        console.error('connection error', err.stack);
    }
    else{
        console.log('connected');
    }
});

client.query("SELECT username FROM accountapplication_user ", (err, res) => {
  if (err) {
    console.error(err.stack);
  } else {
    console.log(res.rows);
  }
});

client.end((err) => {
  if (err) {
    console.error('disconnection error', err.stack);
  } else {
    console.log('disconnected');
  }
});