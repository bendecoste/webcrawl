<?php
//define class
class MySQL{

	private $conId;

	private $host = "100.42.251.163";

	private $user = "bendeco";

	private $password = "password";

	private $database = "crawlbot";

	private $result;

	const OPTIONS=4;

	public function __construct($options=array()){

		if(count($options)!=self::OPTIONS){

			throw new Exception('Invalid number of connection parameters');

		}	

		foreach($options as $parameter=>$value){

			if(!$value){

				throw new Exception('Invalid parameter '.$parameter);

			}

			$this->{$parameter}=$value;

		}

		$this->connectDB();

	}	

	// connect to MySQL

	private function connectDB(){

		if(!$this->conId=mysql_connect("100.42.251.163","bendeco","password")){

			throw new Exception('Error connecting to the server');

		}

		if(!mysql_select_db("crawlbot",$this->conId)){

		throw new Exception('Error selecting database');

		}

	}

	// run query

	public function query($query){

		if(!$this->result=mysql_query($query,$this->conId)){

			throw new Exception('Error performing query '.$query);

		}

		return new Result($this,$this->result);

	}	

	public function escapeString($value){

		return mysql_escape_string($value);

	}

}

// define 'Result' class

	class Result {

		private $mysql;

		private $result;

		public function __construct(&$mysql,$result){

			$this->mysql=&$mysql;

			$this->result=$result;

		}

		// fetch row
	
		public function fetchRow(){

			return mysql_fetch_assoc($this->result);

		}

		// count rows

		public function countRows(){

			if(!$rows=mysql_num_rows($this->result)){

				return false;

			}

			return $rows;
		}

		// count affected rows

		public function countAffectedRows(){

			if(!$rows=mysql_affected_rows($this->mysql->conId)){

				throw new Exception('Error counting affected rows');

			}			

			return $rows;

		}

		// get ID form last-inserted row

		public function getInsertID(){

			if(!$id=mysql_insert_id($this->mysql->conId)){

				throw new Exception('Error getting ID');

			}

			return $id;

		}

		// seek row

		public function seekRow($row=0){

			if(!is_int($row)||$row<0){

				throw new Exception('Invalid result set offset');

			}

			if(!mysql_data_seek($this->result,$row)){

				throw new Exception('Error seeking data');

			}

		}

}

?>



