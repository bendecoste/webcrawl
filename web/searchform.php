<?php
	require_once 'mysql.php';
	echo "<link href=\"css/default.css\" rel=\"stylesheet\" type=\"text/css\" media=\"screen\" />";

	try{

		// connect to MySQL
	
		$db=new MySQL(array
			('host'=>'host','user'=>'user','password'=>'password',
				'database'=>'database'));

		$searchterm=$db->escapeString($_GET['searchterm']);

		$result=$db->query("SELECT * FROM
			Indexed WHERE title LIKE '%$searchterm%'");

		if(!$result->countRows()){
			echo '<div class="maincontainer"><h2>No results were found. Go
	back and try a new search.</h2></div>';
		}

		else{

			// display search results
			echo '<div class="maincontainer"><h2>Your search criteria returned '.$result->countRows().' results.</h2>';

			while($row=$result->fetchRow()){
				echo '<div class="rowcontainer"><p><strong>'.$row['title'].'</strong><p><p><strong>URL:
	</strong><a href="'.$row['url'].'">'.$row['url'].'</a></p></div>';
			}

		}

		echo '</div>';

	} catch(Exception $e){

		echo $e->getMessage();

		exit();

	}

?>

