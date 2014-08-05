PARSED/SCRAPED:
```
DETAILS (184) pre FULL: ['\nOriginal Issue reported by Project Member Reported by waterand...@gmail.com, Mar 8, 2011 - ', '\r\n\r\n\r\nProject Member
 Reported by waterandbirds@gmail.com, Mar 8, 2011 \r\n', '\n1. ', ' (etc).\r\n2. Shows the wiki-markup code for bold, italics etc. (+, _)\r\n3. Think
 also did you do something for <h ref> anchor tags.\r\n\r\n', '\nThat this wiki markup is stripped out.\r\n\r\nWhat version of the product are you us
ing? On what operating system?\r\n9-3-11 build 89\r\n\r\nPlease provide any additional information below.\r\n\r\n\r\n Mar 8, 2011 Project Member #1 m
ark.woolston@csiro.au \r\n(No comment was entered for this change.)\r\n Status: Accepted\n']
DETAILS (184): pre:
Original Issue reported by Project Member Reported by waterand...@gmail.com, Mar 8, 2011 -
DETAILS (184): a: https://code.google.com/p/ala-collectory/issues/detail?id=23
DETAILS (184): b: What steps will reproduce the problem?
DETAILS (184): a: http://collections.ala.org.au/ws/collection/co12
DETAILS (184): b: What is the expected output? What do you see instead?
```

RE-CONSTRUCTED:
(a: meas HTML link, b: means text will be in bold)
```
'\nOriginal Issue reported by Project Member Reported by waterand...@gmail.com, Mar 8, 2011 - ',
a: https://code.google.com/p/ala-collectory/issues/detail?id=23
'\r\n\r\n\r\nProject Member Reported by waterandbirds@gmail.com, Mar 8, 2011 \r\n',
b: What steps will reproduce the problem?
'\n1. ',
a: http://collections.ala.org.au/ws/collection/co12
' (etc).\r\n2. Shows the wiki-markup code for bold, italics etc. (+, _)\r\n3. Think also did you do something for <h ref> anchor tags.\r\n\r\n',
b: What is the expected output? What do you see instead?
'\nThat this wiki markup is stripped out.\r\n\r\nWhat version of the product are you us ing? On what operating system?\r\n9-3-11 build 89\r\n\r\nPlease provide any additional information below
.\r\n\r\n\r\n Mar 8, 2011 Project Member #1 m ark.woolston@csiro.au \r\n(No comment was entered for this change.)\r\n Status: Accepted\n'
```

see [https://code.google.com/p/ala/issues/detail?id=184](https://code.google.com/p/ala/issues/detail?id=184) for visual check/comparison.

---

# UPDATES re-construction/re-assembly

PARSED/SCRAPED:
```JSON
     {
	 updates-elements: [
	     {
		 b: {
		     text: "Owner:"
		 }
	     },
	     {
		 br: { }
	     },
	     {
		 b: {
		     text: "Cc:"
		 }
	     },
	     {
		 br: { }
	     },
	     {
		 b: {
		     text: "Labels:"
		 }
	     },
	     {
		 br: { }
	     }
	 ],
	 updates-full: [
	     " ",
	     " chris.go...@gmail.com ",
	     " ",
	     " -chris.go...@gmail.com CoolDa...@gmail.com ",
	     " ",
	     " -Priority-Medium Priority-High ",
	     " "
	 ]
     }
```

RE-CONSTRUCTED:
```
# Owner was assigned to chris.go...@gmail.com
 Owner: chris.go...@gmail.com

# Cc chris.go...@gmail.com was removed (-), and CoolDa...@gmail.com was added
    Cc: -chris.go...@gmail.com CoolDa...@gmail.com

# priority was changed from Medium to High
Labels: -Priority-Medium Priority-High
```