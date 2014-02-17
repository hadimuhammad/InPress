InPress
=======

This web-based application will allow students in various universities to respond to real-time questions posted by their professor using their computer or mobile device. 

Finished functionality:

Instructor: Modify Course, assessment, questions
Student: View the Course, assessment, questions that are available to them. And answer the questions.


Timeline of Features: 

Feburary 12/2014 - Ability to Record Answers

Features Needed:

- Using LaTex to store Questions and Answers
- Short Answer Checking (Data Analysis)
- Security (HTTPS, POST Data)


InPress - Reading Week Plan
=====


Hi Guys, 

Lets focus on completing our Capstone by the end of reading week. That will give us one month to test and iron out any bugs we might have. Also, that will give us one month to  focus on our Revision 1 Presentation and Documentation (Remember we have other projects, 4TB3 and 4F03 to work on in March). 

Below is what we still have to do: 

1) Data Analysis
- Attendance (Who completed the assessment?)
- (Short Answer) Most Common Answers (What are the most common answers?)
- (Multiple Chice) Who picked what answer? Bar Graph with distribution
- Need to probably add more data analysis…Will have to think about this further….

2) Instructor Side 
- View Class -> What student numbers are enrolled in the class? 
- Add/Remove Student Numbers -> Interface to add and remove student numbers
- UI Cleanup -> Whenever we add delete a question or add a question, the assessment get collapsed. We need the assessment to stay expanded. Also,  Justin suggested last week we separate posted and un-posted assessment. Will need a discussion there. 

3) Student Side
- Assessments -> If you have a posted assessment  in the past, it doesn’t work. Need to fix this requirement
- UI Cleanup for Answer Questions -> Need to beautify the viewassessment.html file. This was done last minute for our Rev 0, and we need to make it look better than it is. 
- Student Answer -> Need an interface that allows students to see what they answered, and if they were correct or wrong. If they were wrong, it should state that, and give the right answer. 
- After students complete an assessment, it should tell them that they have completed it, and send them to iv) if they chose to. 
	
4) Security
- HTTPS Protocol
- Only allow one student number login concurrently
 
5) QA Testing 
- We need to execute all the test cases we have created in our test plan, and make sure all the manual testing works
- Need to create the test cases using the Selenium Framework to ensure that we have some sort of automated testing implemented
- Need to stress test the product so it can withstand >200 students at a time. 
