
# Adaptive Applications (CS7IS5)

## Adaptive GRE learning Application

**Team Royal**

<p align="center">
  <img src="https://github.com/Shritesh99/royal/blob/main/imgs/Aspose.Words.64c412b8-9a48-4854-aa05-7d4730dc14e5.001.jpeg">
</p>

**Team members**

Siyu Liao - 22323209 - liaosi@tcd.ie
Haoxian Liu - 22322820 - liuha@tcd.ie
Rui Zhao - 22328549 - zhaoru@tcd.ie
Pallavit Aggarwal - 22333721 - aggarwpa@tcd.ie
Shritesh Jamulkar - 22324542 - <jamulks@tcd.ie>

## Introduction

**Setting the stage:**

There are multiple applications available online which provide the trending “e-learning” experience. Learning style is something that is unique to an individual and this provides a big open field to apply the concepts of adaptability and explore the various topics in the subject of Adaptive applications to create a platform that adapts to the users and provides scrutability to the user on the interface. By tailoring the content and learning path to each learner's strengths, weaknesses, and interests, the adaptive application can help users achieve a deeper understanding of the subject matter, improve retention, and develop more effective problem-solving skills

**Inspiration:**

There are multiple systems like EASL, WITS, WEB-PVT, ELEKTRA, OPEN-EDX, ELM-ART, PERSO and ActiveMath, that we take inspiration from and refer to while thinking about this problem space and our need to extend it. We take a different approach here by integrating the latest openai-api as a knowledge base and intelligent system.

## Methodology - System Design & Implementation

***User Modelling:***

To understand and model our user better, we first choose the right technique to represent and maintain our user models. The techniques are largely conceptualized as Explicit, Implicit or a Blended approach, and the model types can be feature based, overlay based and stereotype based .

While there are extensive examples on feature based user modelling and it has the added advantage of being simple in its approach, the Overlay user modelling and Stereotype user modelling approaches fit our topic of learning the best.

Overlay models capture a user's knowledge and proficiency in specific subject areas, while stereotype models categorize users based on common characteristics or behaviour patterns. By leveraging these models, our application can adapt the content, instructional strategies, and difficulty levels to suit the individual needs and preferences of each learner. This leads to a more engaging and efficient learning experience.

The idea behind using overlay and stereotype user modelling is to optimize the learning process by focusing on areas where the learner needs improvement or reinforcement. This can save both time and resources by avoiding unnecessary repetition of already mastered content and targeting the specific needs of each learner more accurately.

The User Profile data structure is shown in the following image: The User Modeling structure is shown as below:

<p align="center">
  <img src="https://github.com/Shritesh99/royal/blob/main/imgs/Aspose.Words.64c412b8-9a48-4854-aa05-7d4730dc14e5.002.jpeg">
</p>

The above two figures are a comprehensive user profile structure that captures various aspects of a learner's skills, performance, learning style, motivation, goals, and personal information.

**Overlay Modelling:**

- The “Skills” property can be used for overlay modelling, as it represents the user's knowledge and proficiency in different subject areas (e.g., geometry, algebra, ratio). By comparing the user's performance in these topics (right, wrong, time taken per question, actual\_accuracy, total\_questions), we can tailor the content and difficulty levels to address their strengths and weaknesses, ensuring an efficient and effective learning experience.

**Stereotype Modelling:**

- We use the learning\_style, motivation\_score, and user\_information properties to create stereotype user models. By clustering users based on their learning styles (active, reflective, intuitive, verbal, visual, sequential, global) and motivation scores, we categorize them into predefined groups with common characteristics. This helps us identify the most suitable learning materials, activities, and teaching strategies for each group, leading to a more engaging and personalized experience.

**Personalized Learning Paths and Goals:**

- The Goals property is used to create personalized learning paths for each user. By setting specific goals for each subject (topic\_name, goal\_accuracy, total\_questions) and global goals (total\_score, total\_accuracy), we guide the user through a tailored learning journey that aligns with their objectives and keeps them motivated to achieve their targets.

**Performance Monitoring and Feedback:**

- We utilize the User\_Performance property to monitor the user's progress and by analysing average accuracy, average time spent, average daily questions, and total score, we give users insights into their strengths and areas for improvement, helping them adjust their learning strategies and stay on track to achieve their goals.

**Motivation and Engagement:**

- The motivation\_score property is used to track and manage user motivation. By adjusting the score based on their performance and interactions, we provide personalized interventions, such as encouragement, reminders, or tailored content, to keep users engaged and motivated throughout their learning journey.

**Demographic-based Adaptations:**

- The user\_information property, which includes gender, name, nickname, and date of birth, is used to personalize the user interface or choose examples and learning materials that are more relevant or relatable to the user's age, gender, or cultural background.

We add another data structure on top of this to track the user’s interaction. This enhances our adaptive application’s ability to tailor the learning experience based on the user’s real-time performance, engagement, and progress.
<p align="center">
  <img src="https://github.com/Shritesh99/royal/blob/main/imgs/Aspose.Words.64c412b8-9a48-4854-aa05-7d4730dc14e5.004.jpeg">
</p>


**Real-time Adaptation:**

- The Timestamp, login\_timestamp, Time\_spent\_today, Total\_questions\_today, and Accuracy\_today properties provide insights into the user's engagement and performance during a specific session. By analysing this data in real-time, our application can make immediate adjustments to the content, difficulty levels, and instructional strategies, ensuring a more responsive and personalized learning experience.

**Progress Tracking and Feedback:**

- The Goals\_achieved property, which includes subject goals and global goals, helps track the user's progress towards their learning objectives. By monitoring the goals achieved, the application provides timely feedback and encouragement to keep users motivated and informed about their progress. Also, internally it helps identify areas where the user may need additional support or guidance.

**Test Performance Analysis:**

- The test property provides detailed information about the user's performance in assessments, including total score, total time taken, and individual question data (topic, difficulty level, correctness, time taken). By analysing this information, we identify patterns and trends in the user's test performance, uncovering strengths and weaknesses that can be addressed through personalized content and learning strategies.

**Content Recommendation and Sequencing:**

- The questions property within the test object offers insights into the user's performance on specific topics and difficulty levels. By leveraging this data, the machine learning model can optimally build on the user's existing knowledge and addresses their learning needs.

In the user profile structure above, we use a *blended user modelling approach*. Here's how:

**Explicit User Modelling:** The user\_information property, where the user provides their gender, name, nickname, and date of birth, is an example of explicit user modelling. Additionally, the learning\_style property, which captures the user's preferred learning style, can also be considered explicit if the user explicitly provides this information through a questionnaire or self-assessment.

**Implicit User Modelling:** The User\_Interaction and User\_Performance properties are examples of implicit user modelling. These properties capture information about the user's behaviour and performance (e.g., time spent, questions answered, accuracy, test performance, goals achieved) as they interact with the system. This data is collected automatically and does not require direct user input.

By combining both explicit and implicit user modelling techniques, our application creates a comprehensive and accurate user model that effectively supports personalization and adaptation.

### Implementation

Having a diverse array of User modelling features enables us to create a fine-tuned system and environment.

On the start screen, we first gather some background information like Name, Age, Ethnicity etc, this gives the user the feeling of ownership from the onset.

Post this, we start gathering the relevant inputs required by the user model. These inputs, ultimately are stored in CSV files namely learning\_style.csv, motivation\_level.csv and skill\_level.csv which have their own simplistic schemas defined. These are used to create a user model,

### Learning Style

Now, we determine the Learning style of the user. To use this we employ the Felder-Silverman Learning Style Model. FSLSM categorizes learning styles based on a student's preferences in four dimensions: sensing-intuitive, visual-verbal, active-reflective, and sequential-global. The model assumes that individuals have a preferred way of learning, and by understanding their preferences, educators can create learning experiences that are more effective and engaging.

The following are the questions we ask for personality identification, **FSLSM** helps

1. *When starting a new project, do you prefer to dive right in or take some time to plan and gather information? **(Sensing-Intuitive)***
	A. Dive right in
	B. Take time to plan and gather information
2. *Do you rely on your senses to understand information or do you tend to rely more on intuition and abstract concepts? **(Visual-Verbal)***
	A. Rely on senses and observations
	B. Rely on abstract concepts and intuition
3. *Do you find it helpful to use diagrams or other visual aids when learning new information?( **Visual- Verbal)***
	A. Prefer pictures, diagrams, and other visual aids
	B. Prefer written or spoken explanations
4. *Do you prefer to learn things in a step-by-step, sequential manner or do you prefer to see the big picture and make connections between ideas? **(Sequential-Global)***
	A. Prefer to learn in a step-by-step, linear fashion
	B. Prefer to see the big picture and make connections between ideas
5. *Do you tend to remember things better when you write them down or when you hear them spoken aloud? **(Sensing-Intuitive)***
	A. Remember better when writing things down
	B. Remember better when hearing things spoken aloud
6. *Do you prefer to work alone or in groups when learning new material? **(Active-Reflective)***
	A. Prefer to work alone
	B. Prefer to work in groups
7. *When you encounter a problem, do you prefer to try out different solutions until you find one that works or do you prefer to think through the problem and develop a solution before acting?**(Active-Reflective)***
	A. Try out different solutions until one works
	B. Think through the problem before acting
8. *Do you enjoy hands-on activities or experiments when learning new material? **(Visual-Verbal)***
	A. Enjoy hands-on activities and experiments
	B. Prefer more abstract and theoretical learning
9. *Do you find it helpful to discuss and debate ideas with others when learning new information? **(Active- Reflective)***
	A. Find it helpful to discuss and debate ideas with others
	B. Prefer to reflect and think through ideas alone
10. *When reading a textbook or article, do you prefer to highlight and take notes or do you prefer to read and absorb the information without marking it up? **(Visual-Verbal)***
	A. Prefer to highlight and take notes
	B. Prefer to read and absorb information without marking it up

Based on a student's responses to these questions, their learning style can be identified according to the Felder-Silverman model. For example, if a student consistently selects visual options over verbal ones, they may have a visual learning style. Similarly, if a student prefers working alone and reflecting on ideas, they may have a reflective learning style. By understanding a student's learning style, we tailor the questions to better match the student's needs, resulting in improved learning outcomes and engagement. The data from the input is interpreted by taking mean of the values from the inputs received here. This data is stored in learning\_style.csv in the schema like: ID, SI, VV, AR, SG.

Here SI (Sensing-Intuition), VV (Visual-Verbal), AR (Active-Reflective) and SG (Sequential-Global) are groups based on which we will ultimately tweak the type of questions and even the type of hints or answers and explanations that we provide.

### Motivation

Now that we have determined the type of questions that the user would likely respond to, our next parameter is Motivation. Motivation would enable us set the difficulty level for the user, and monitoring Motivation over the course of user’s interaction with the system will enable us to alter the question levels to manage user’s involvement.

It is calculated by the following questions:

Question1: Has user taken GRE before? (1 - yes 0 – no) Question2: What has the user scored? (out of 170)

Question3: What score do you want to achieve next? (out of 170) Question4: When are planning to take GRE?

Question5: How long was it taken?

Question6: How many times has he taken it overall?

The answers for Q1 can be 1/0 showing user’s GRE history as an affirmation or negation respectively. Value for Q2 and Q3 is out of 170 total score of GRE quant, Q4, Q5 are in months, and Q6 is a number which cannot be >10

Assuming we get the following input : {'Q1': 1, 'Q2': 155, 'Q3': 169, 'Q4': 1, 'Q5': 3, 'Q6':9}which implies that the user has taken GRE before, score 155 before, wants to score a whopping 169 now, will be taking the GRE in a month’s time again, took it 3 months ago and has given it a total number of 9 times, meaning this would be the last attempt. A do or die situation!

We now calculate a motivation score, using a simple formula we decided withing us, that takes the max of Q 3 or 4, subtracts the magnitude values of 4,5 and 6 and normalizes the score by dividing it with 170 which is the total marks. This is stored in the motivation\_level.csv with the schema ID, motivation\_score. The motivation scores are from 0-1 range, 1 being the most motivated and 0 being the least motivated.

### Skill Level Judgement

Finally a diagnostic test with 10 questions is done, to gauge the user’s skills in different topics. The skill is calculated out from 0-10, and the higher the number the better the user is in that topic. It is calculated as score = ( topic\_weight + (time\_weight / time) – (diff\_weight \* difficulty ) + correct\_weight \* (1 if correct else 0) )

The time\_weight is divided by the time taken to answer a question to incorporate the time efficiency of the user in the score calculation. By dividing the time\_weight by the time taken, we are rewarding users who can answer questions faster while maintaining accuracy. The faster a user answers a question, the more significant the contribution of the time\_weight will be to the overall score.

The diff\_weight is multiplied by the difficulty to account for the level of challenge a question presents in the score calculation. By multiplying the diff\_weight by the difficulty, the formula takes into consideration the complexity of the question, giving a higher penalty to the score for more difficult questions.

### User Profile

Based on the implemented method for building a user model, we can obtain a comprehensive user profile for each individual. To train the adaptive model, we generated mock profile information for 1000 users. In the following sections, we will present the user profile map from four crucial perspectives:

1. **Background Information**

This includes demographic data, such as age and gender, which can provide insights into the user's characteristics and preferences. For example:

<p align="center">
  <img src="https://github.com/Shritesh99/royal/blob/main/imgs/Aspose.Words.64c412b8-9a48-4854-aa05-7d4730dc14e5.005.jpeg">
</p>

2. **Learning Style Data**

This aspect encompasses the user's preferred learning styles based on the FSLSM model, such as visual, active, or sensing, which can help tailor the learning experience to suit their needs. The following figure shows the 1000 users’ distribution of learning styles:
<p align="center">
  <img src="https://github.com/Shritesh99/royal/blob/main/imgs/Aspose.Words.64c412b8-9a48-4854-aa05-7d4730dc14e5.006.png">
</p>

After analyzing the figure, it is evident that we have endeavored to achieve a balanced distribution of data for each learning style pair. This approach ensures that our model can effectively comprehend and learn the unique characteristics of each user class, enabling it to make informed and accurate judgments.

3. **Skill Data**

This reflects the user's proficiency level in a specific subject or skill, which can assist in determining the appropriate level of difficulty for the learning topics.

<p align="center">
  <img src="https://github.com/Shritesh99/royal/blob/main/imgs/Aspose.Words.64c412b8-9a48-4854-aa05-7d4730dc14e5.007.png">
</p>

Upon examining the figure, it is apparent that we have striven to achieve a balanced distribution of data for each mathematical topic. This approach has enabled us to comprehensively cover the characteristics of users with varying skill levels, thus facilitating the creation of an effective and personalized learning experience for each user.

4. **Motivation Score**

This indicates the user's level of motivation or interest in the subject matter, which can assist in creating engaging and relevant learning experiences. For example:

<p align="center">
  <img src="https://github.com/Shritesh99/royal/blob/main/imgs/Aspose.Words.64c412b8-9a48-4854-aa05-7d4730dc14e5.008.jpeg">
</p>

### Adaptive Workflow

<p align="center">
  <img src="https://github.com/Shritesh99/royal/blob/main/imgs/Aspose.Words.64c412b8-9a48-4854-aa05-7d4730dc14e5.009.jpeg">
</p>

The system architecture consists of several interconnected modules designed to process and generate questions based on user profiles and predicted difficulty levels. The architecture can be described as follows:

1. User Profile Generation: This module is responsible for generating user profiles. User profiles are created, and relevant data is stored for further processing.
2. User Modeling Algorithm: This module takes the generated user profiles as input and builds user models based on a user-modeling algorithm. These user models are designed to represent individual users' learning preferences and abilities.
3. Machine Learning Training: In this module, the user models are trained with a machine learning algorithm using difficulty levels as labels. The training process generates trained user models that can predict the appropriate difficulty levels for individual users.
3. Trained User Models Storage: The trained user models are stored in a database to be used later in the prediction process.
3. Difficulty Level Prediction: This module loads the stored trained user models and predicts the difficulty levels for individual users. The predicted difficulty levels are determined based on each user's unique characteristics and learning preferences.
3. GRE Question Generation: In this module, the user models and predicted difficulty levels are used as input to generate GRE questions tailored to individual users. These questions are designed to match the user's skill level and learning preferences.

The architecture is designed to provide a personalized experience for users by predicting the appropriate difficulty levels for GRE questions based on their unique learning preferences and abilities. It integrates Monte Carlo methods, user-modeling algorithms, machine learning, and question generation techniques to deliver a tailored practice experience for each user.

### OpenAI – GPT4

Based on our implementation, our system utilizes a combination of machine learning and GPT-4 technology to generate GRE questions that are tailored to each user's skill level and learning goals.

To achieve this, our system first employs a machine learning model to analyze user data and generate key tokens related to topics, difficulty levels, and other relevant factors. These tokens are then combined to form a prompt that is passed to the GPT-4 model, which generates the final GRE question.

By leveraging the power of machine learning and GPT-4 technology, our system is able to deliver personalized and effective learning experiences for each user. The machine learning model analyzes user data to generate personalized prompts that are optimized for their specific learning needs and preferences, while the GPT-4 model generates high-quality GRE questions that challenge and engage users at their level.

Overall, our approach to question generation is a key feature that sets our platform apart, enabling us to provide a highly personalized and effective learning experience that empowers users to achieve their learning goals and excel on the GRE.

### System Architecture

Here is the figure of our system architecture:

<p align="center">
  <img src="https://github.com/Shritesh99/royal/blob/main/imgs/Aspose.Words.64c412b8-9a48-4854-aa05-7d4730dc14e5.010.png">
</p>

**Frontend:** As illustrated in the above figure, our system's front-end Test Interface employs a combination of React and Next.js technologies to deliver an intuitive and user-friendly experience. These technologies enable us to create a highly responsive interface that caters to the unique needs of each user.

**Middleware:** we rely on graphQL APIs to store and manage the data that drives our system. This includes user profiles, GRE topics, and other relevant information necessary for creating an effective and personalized learning experience for each user. The use of graphQL APIs facilitates seamless data retrieval and manipulation, allowing us to efficiently manage large volumes of data with ease.

**Backend:** component of our system is built using the Django framework and comprises two engines: the Test Engine and User Assessment Engine. These engines are responsible for processing user data and generating personalized learning experiences for each user. The Test Engine facilitates user interaction with the system by providing a wide range of test options tailored to the user's skill level and learning style. The User Assessment Engine, on the other hand, analyzes user performance data to generate personalized recommendations and feedback, enabling users to continually improve their skills and knowledge.

## Metrics and Discussion

### UI Interface

1. ***Login Page***

<p align="center">
  <img src="https://github.com/Shritesh99/royal/blob/main/imgs/Aspose.Words.64c412b8-9a48-4854-aa05-7d4730dc14e5.011.png">
</p>

2. **Motivation Questionnaire Page**
<p align="center">
  <img src="https://github.com/Shritesh99/royal/blob/main/imgs/Aspose.Words.64c412b8-9a48-4854-aa05-7d4730dc14e5.013.jpeg">
</p>

3. ***Learning Style Page***
<p align="center">
  <img src="https://github.com/Shritesh99/royal/blob/main/imgs/Aspose.Words.64c412b8-9a48-4854-aa05-7d4730dc14e5.015.png">
</p>

4. **Testing Page**
<p align="center">
  <img src="https://github.com/Shritesh99/royal/blob/main/imgs/Aspose.Words.64c412b8-9a48-4854-aa05-7d4730dc14e5.017.png">
</p>

The four images presented above showcase the primary interfaces of our web platform, including the landing page, questionnaire page, and test page. Our team has prioritized simplicity and efficiency in the design of these pages, focusing on providing users with a straightforward and intuitive interface that facilitates a seamless learning experience.

Our implemented pages do not feature excessive or unnecessary functionalities, instead focusing on delivering key features such as collecting user profiles, administering tests (comprising 10-20 questions with a countdown timer), and enabling adaptive looping. By keeping the design simple and streamlined, we have ensured that users can navigate the platform with ease, and that the learning process is as straightforward and effective as possible.

### Database

The figures below show the complete range of information stored in our database. During the design phase

of the system, we placed great importance on creating a well-structured and efficient database table structure. The structure consists of four key modules: authorization, mock\_test, social\_auth, and questions.

The authorization module facilitates the user authentication and authorization process for secure and reliable access to the platform. mock\_test stores information related to mock tests, including test type, duration, and difficulty level. social\_auth handles the social media authentication process, allowing users to quickly and easily log in to the platform using their social media accounts. Finally, the questions module stores questionnaires as well as extensive information related to GRE math questions, including question types, difficulty levels, and subject topics.

<p align="center">
  <img src="https://github.com/Shritesh99/royal/blob/main/imgs/Aspose.Words.64c412b8-9a48-4854-aa05-7d4730dc14e5.020.png">
</p>
<p align="center">
  <img src="https://github.com/Shritesh99/royal/blob/main/imgs/Aspose.Words.64c412b8-9a48-4854-aa05-7d4730dc14e5.021.png">
</p>

### Skill Assessment Evaluation

In the illustrated figure below, we present the learning data results for user 123 on our platform. The horizontal axis denotes the number of tests taken by the user, while the vertical axis represents changes in the user's skill level across different math topics.

By analyzing the graph, we can observe that as user 123 continues to practice on our platform everyday, their mastery level gradually increases across various math topics. This trend highlights the effectiveness of our platform in facilitating user learning and improvement over time. The graph provides valuable insights into the user's performance and progress, allowing us to provide personalized feedback and recommendations to optimize their learning experience.

<p align="center">
  <img src="https://github.com/Shritesh99/royal/blob/main/imgs/Aspose.Words.64c412b8-9a48-4854-aa05-7d4730dc14e5.022.jpeg">
</p>

### Motivation Level Evaluation

1. ***Improvement***

The graph below displays the data of a user who is actively engaging in learning and practice on our platform every day. The horizontal axis represents various mathematical topics, while the vertical axis indicates the corresponding changes in skill level over time.

Upon analyzing the graph, we can observe a clear trend of the user's skill level gradually increasing across different math topics as they actively practice on our platform. This observation highlights the effectiveness of our platform in facilitating user learning and improvement over time. As the user's skill level improves, they are better able to complete our tests with greater ease, demonstrating the potential of our platform to help users improve their GRE scores.

<p align="center">
  <img src="https://github.com/Shritesh99/royal/blob/main/imgs/Aspose.Words.64c412b8-9a48-4854-aa05-7d4730dc14e5.023.png">
</p>

2. ***Decrement***

Upon analyzing the graph, we can observe that the user's learning results do not exhibit a steady improvement over time. Although the user is initially active and serious in their learning approach, their score briefly improves before decreasing due to their lack of consistent practice. This trend highlights the importance of regular and sustained practice in achieving lasting improvements in skill level.

While our platform is designed to facilitate personalized and adaptive learning experiences, it ultimately requires users to take an active and consistent approach to learning to achieve optimal outcomes. The graph demonstrates the need for users to remain committed to their learning goals and to consistently engage with our platform to maximize the benefits it can provide.

<p align="center">
  <img src="https://github.com/Shritesh99/royal/blob/main/imgs/Aspose.Words.64c412b8-9a48-4854-aa05-7d4730dc14e5.024.png">
</p>

## Future Work and Conclusion

Our app provides a highly flexible and personalized way for GRE test-takers to practice math questions, with the platform dynamically adjusting the difficulty and type of questions based on users' personal and performance information.

While our app is already highly functional, we are still considering how we can further improve our platform in the future. We plan to add more practice modes and question types to meet users' diverse needs, including the addition of questions with images, as our current GRE questions do not include any visual aids.

Additionally, we will strengthen our ability to collect and analyze user personal information to provide better personalized practice services. Furthermore, we also plan to add social features and competition modes to increase user engagement and retention, such as leaderboards, friend interactions, and discussion areas.

Overall, we prioritize the user experience and needs, and will continue to work towards improving our platform to better serve our users.

### References

1. RAYNER, S. (2001). Cognitive styles and learning styles. International Encyclopedia of Social & Behavioral Sciences. UK: Elsevier Science Ltd.

2. E. Wenger, Artificial intelligence and tutoring systems: computational and cognitive approaches to the communication of knowledge: Morgan Kaufmann Publishers Inc. San Francisco, CA, USA, 1987.

3. P. Brusilovsky, "Adaptive Hypermedia," User Modeling and User-Adapted Interaction, vol. 11, pp. 87-110, 2001.

4. D. Charles, "Enhancing Gameplay: Challenges for Artificial Intelligence in Digital Games," in 1st World Conference on Digital Games, University of Utrecht, The Netherlands, 2003.

5. W. L. Johnson, N. Wang, and S. Wu, "Experience with serious games for learning foreign languages and cultures," in SimTecT Conference., Australia, 2007.

6. P. Moreno-Ger, D. Burgos, J. L. Sierra, and B. FernándezManjón, "A Game-Based Adaptive Unit of Learning with IMS Learning Design and <e-Adventure>. ," in Second European Conference on Technology Enhanced Learning (EC-TEL 2007), Crete, Greece., 2007.

7. FELDER, R. M. & SILVERMAN, L. K. (1988). Learning and teaching styles in engineering education. Engineering Education, 78(7), 674-681. Preceded by a preface in 2002.

8. FELDER, R. M., SILVERMAN, L. K. & SOLOMON, B.A (1996). Index of Learning Styles (ILS). North Carolina State University.

9. FELDER, R. M. & SPURLIN, J. (2005). Applications, reliability and validity of index of learning styles. International Journal of Engineering Ed., 21(1), 103-112.

10. Peirce, N.; Conlan, O.; Wade, V.; Adaptive educational games: Providing non-invasive personalised learning experiences, Digital Games and Intelligent Toys Based Education, Second IEEE International Conference on, pp. 28-35, 2008, IEEE.

11. User Models for Adaptive Hypermedia and Adaptive Educational, by Brusilovsky and Millán, from Adaptive Web, LNCS 4321, Brusilovsky, Kobsa and Nejdl, 2007

12. Stereotypes, Student Models and Scrutability, Intelligent Tutoring Systems, 5th International Conference, ITS 2000, Montréal, Canada, June 19-23, 2000

13. Conlan, O., Staikopoulos, A., Hampson, C., Lawless, S., O'Keeffe, I. (2013) The Narrative Approach to Personalisation, New Review of Hypermedia and Multimedia, 19, (2), p132 – 157

14. Caprotti, O., & Cohen, A. M. (1998). Draft of the open math standard. (Open Math Consortium, http://www.nag.co.uk/projects/OpenMath/omstd/)

15. Char, B., Fee, G., Geddes, K., Gonnet, G., & Monagan, M. (1986). A tutorial introduction to MAPLE. Journal of Symbolic Computation, 2(2), 179-200.

16. Cohen, A., Cuypers, H., & Sterk, H. (1999). Algebra interactive! Springer-Verlag
