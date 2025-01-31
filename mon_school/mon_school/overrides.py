import frappe

from school.lms.doctype.exercise.exercise import Exercise as _Exercise
from school.lms.doctype.exercise_submission.exercise_submission import ExerciseSubmission as _ExerciseSubmission
from school.lms.doctype.lms_batch_membership.lms_batch_membership import LMSBatchMembership as _LMSBatchMembership
from school.lms.doctype.cohort_subgroup.cohort_subgroup import CohortSubgroup as _CohortSubgroup

from . import livecode

class Exercise(_Exercise):
    def before_save(self):
        self.image = livecode.livecode_to_svg(self.answer)

class ExerciseSubmission(_ExerciseSubmission):
    def before_save(self):
        self.image = livecode.livecode_to_svg(self.solution)

class LMSBatchMembership(_LMSBatchMembership):
    def validate_membership_in_different_batch_same_course(self):
        if self.member_type == "Mentor":
            return
        else:
            return super().validate_membership_in_different_batch_same_course()

class CohortSubgroup(_CohortSubgroup):
    def get_students_with_score(self):
        students = self.get_students()
        scores = self.get_scores()

        for s in students:
            s.score = scores.get(s.name, 0)
        return sorted(students, key=lambda s: s.score, reverse=True)

    def get_scores(self):
        rows = frappe.get_all("Student Score Activity",
            filters={"subgroup": self.name},
            fields=["user", "sum(score) as score"],
            group_by="user",
            page_length=1000)
        return {row.user: row.score for row in rows}
