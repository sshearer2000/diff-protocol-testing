"""# Function to rename long-worded columns"""

def rename_col(csv, og_name, new_name):
    csv.rename(columns={og_name:new_name},inplace=True)

"""# Rename columns"""

rename_col(stud,'Timestamp','time')
rename_col(stud,'Participant ID','id')
rename_col(stud, 'What topics did you cover in class this week?','topics_covered')
rename_col(stud,'What kinds of activities did you focus on out of class this week?  [Reading/Research]','reading_research')
rename_col(stud, 'What kinds of activities did you focus on out of class this week?  [Continuing/Finishing In-Class Work]','finishing_class_work')
rename_col(stud, 'What kinds of activities did you focus on out of class this week?  [Homework Problems/Assignments]','homework')
rename_col(stud, 'What kinds of activities did you focus on out of class this week?  [Out-of-Class Labs]', 'out_of_class_labs')
rename_col(stud, 'What kinds of activities did you focus on out of class this week?  [Multi-Week Project Experience]','multi_week_project')
rename_col(stud, 'What kinds of activities did you focus on out of class this week?  [Other]','other_outside_class')
rename_col(stud, 'What concepts/activities did you or your peers struggle most with this week?','struggle_concepts')
rename_col(stud, 'What questions did you or your peers raise to your instructor/TAs this week?','questions_raised')
rename_col(stud, 'Were there any questions from your peers that surprised you this week?','surprise_questions')

rename_col(profta, 'Timestamp','time')
rename_col(profta,'Participant ID', 'id')
rename_col(profta, 'What is your role in the course you are reflecting on? ','role')
rename_col(profta, 'What topics did you cover this week?','topics_covered')
rename_col(profta, 'What kinds of activities did your students focus  on this week out of class?  [Reading/Research]','reading_research')
rename_col(profta, 'What kinds of activities did your students focus  on this week out of class?  [Continuing/Finishing In-Class Work]','finishing_class_work')
rename_col(profta, 'What kinds of activities did your students focus  on this week out of class?  [Homework Problems/Assignments]','homework')
rename_col(profta, 'What kinds of activities did your students focus  on this week out of class?  [Out-of-Class Labs]', 'out_of_class_labs')
rename_col(profta, 'What kinds of activities did your students focus  on this week out of class?  [Multi-Week Project Experience]','multi_week_project')
rename_col(profta, 'What kinds of activities did your students focus  on this week out of class?  [Other]','other_outside_class')
rename_col(profta, 'By observation, what concepts or processes did students struggle with?','struggle_concepts')
rename_col(profta, 'What questions did students raise this week?','questions_raised')
rename_col(profta, 'Which student questions were surprising to you?','surprise_questions')

"""# Replace NA values with strings"""

stud.topics_covered = stud.topics_covered.replace({None:'NA'})
stud.reading_research = stud.reading_research.replace({None:'NA'})
stud.finishing_class_work = stud.finishing_class_work.replace({None:'NA'})
stud.homework = stud.homework.replace({None:'NA'})
stud.out_of_class_labs = stud.out_of_class_labs.replace({None:'NA'})
stud.multi_week_project = stud.multi_week_project.replace({None:'NA'})
stud.other_outside_class = stud.other_outside_class.replace({None:'NA'})
stud.struggle_concepts = stud.struggle_concepts.replace({None:'NA'})
stud.questions_raised = stud.questions_raised.replace({None:'NA'})
stud.surprise_questions = stud.surprise_questions.replace({None:'NA'})

profta.topics_covered = profta.topics_covered.replace({None:'NA'})
profta.reading_research = profta.reading_research.replace({None:'NA'})
profta.finishing_class_work = profta.finishing_class_work.replace({None:'NA'})
profta.homework = profta.homework.replace({None:'NA'})
profta.out_of_class_labs = profta.out_of_class_labs.replace({None:'NA'})
profta.multi_week_project = profta.multi_week_project.replace({None:'NA'})
profta.other_outside_class = profta.other_outside_class.replace({None:'NA'})
profta.struggle_concepts = profta.struggle_concepts.replace({None:'NA'})
profta.questions_raised = profta.questions_raised.replace({None:'NA'})
profta.surprise_questions = profta.surprise_questions.replace({None:'NA'})
