SCHOOL_CODE = None

SECTIONS = 'FGHIJKLM'
STUDENTS_PER_SECTION = 40
ROLLS = ['00' + str(x) if x > 9 else '0' + str(x) for x in range(1, 100)]

BASE_URL = 'http://results.sofworld.org/results'
