<?php

class Common
{
	var $conn;
	var $debug;

	var $server="database.cse.tamu.edu";
	var $dbname="hayleyeckert";
	var $user="hayleyeckert";
	var $pass="#2018Golfer#";

	function Common($debug)
	{
		$this->debug = $debug;
		$rs = $this->connect($this->user); // db name really here
		return $rs;
	}

// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% */

	function connect($db)// connect to MySQL DB Server
	{
		// Create connection
		$this->conn = new mysqli($this->server, $this->user, $this->pass);

		// Check connection
		if ($this->conn->connect_error) { die("Connection failed: " . $this->conn->connect_error . "<br>\n"); }
		echo "Connected successfully<br>\n";
	}


// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% */

	function executeQuery($sql, $filename) // execute query
	{
		// AS OF 6/17, the DB must be apart of the query such as:
		// INSERT INTO `slupoli`.`wishlist` (`id`, `item`, `cost`) VALUES (NULL, 'airplane - G5', '200000')
		// notice 'slupoli' part

		if($this->debug == true) { echo("Query-> <br>$sql<br>\n"); }
		$rs = $this->conn->query($sql) or die("Could not execute query '$sql' in $filename<br>\n");
		return $rs;
	}

} // ends class, NEEDED!!

?>
