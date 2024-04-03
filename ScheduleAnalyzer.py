import ast

with open('Output.txt', 'r+') as file:
  file.seek(0)
  # Truncate the file (clear its contents)
  file.truncate()

arrayOfDict = []
newValueDict = {}

#O(n)
with open('Input.txt', 'r') as Rfile:
  content = Rfile.read()
  content = content.splitlines()
  #print(content)

for i in range(len(content)):
  #left off here, trying to solve a sample of COMPLETELY EMPTY, but now debating if we should continue or not

  if 'schedule' in content[i].lower():
    schedule = [item.strip() for item in content[i].split('=')]
    newValueDict[schedule[0]] = ast.literal_eval(schedule[1])
  if 'dailyact' in content[i].lower():
    dailyact = [item.strip() for item in content[i].split('=')]
    newValueDict[dailyact[0]] = ast.literal_eval(dailyact[1])
  if 'duration' in content[i].lower():
    duration = [item.strip() for item in content[i].split('=')]
    newValueDict[duration[0]] = duration[1]
  if '--------' in content[i]:
    #len(newValueDict[schdule]) != len(dailyact) or (len(newValueDict[schdule]) == 0 and  len(duration) == 0)

    #[]
    arrayOfDict.append(newValueDict)
    newValueDict = {}

if 'duration' in content[i].lower():
  duration = [item.strip() for item in content[i].split('=')]
  duration_value = duration[1]
  try:
    duration_value = int(duration_value)
    if duration_value < 0:
      raise ValueError("Duration cannot be negative")
    newValueDict[duration[0]] = duration_value
  except ValueError as e:
    print(f"Error: {e}. Skipping negative duration.")

#print(arrayOfDict)
#newdict["person1_schedule"]
#if = then
#person1Dailyact


def calculate_time_interval_manual(start, end):
  start = int(start.replace(":", ""))
  end = int(end.replace(":", ""))
  # Extract hours and minutes for start time
  start_hours = start // 100
  start_minutes = start % 100

  # Convert start time to minutes
  start_total_minutes = start_hours * 60 + start_minutes

  # Extract hours and minutes for end time
  end_hours = end // 100
  end_minutes = end % 100

  # Convert end time to minutes
  end_total_minutes = end_hours * 60 + end_minutes

  # Calculate the difference in minutes
  interval = end_total_minutes - start_total_minutes

  return interval


def time_to_minutes(time_str):
  """Converts a time string HH:MM to minutes since midnight."""
  h, m = map(int, time_str.split(':'))
  return h * 60 + m


def minutes_to_time(minutes):
  """Converts minutes since midnight to a time string HH:MM."""
  return f"{minutes // 60:02d}:{minutes % 60:02d}"


def normalize_schedule(schedule):
  """Convert a schedule into a set of minutes for each day."""
  normalized = set()
  for start, end in schedule:
    start_min = time_to_minutes(start)
    end_min = time_to_minutes(end)
    normalized.update(range(start_min, end_min))
  return normalized


#O(n)
def find_common_availability(schedules):
  """Find common available time slots among all schedules, formatted as requested."""
  # Normalize all schedules to sets of minutes
  #O(n)
  normalized_schedules = {
      person: normalize_schedule(schedule)
      for person, schedule in schedules.items()
  }

  # Find the intersection of minutes across all normalized schedules
  common_minutes = set.intersection(*normalized_schedules.values())
  if not common_minutes:
    return []

  # Sort the common minutes and group them into continuous slots
  common_time_slots = []
  sorted_minutes = sorted(common_minutes)
  slot_start = sorted_minutes[0]
  #O(n)
  for i in range(1, len(sorted_minutes)):
    if sorted_minutes[i] != sorted_minutes[i - 1] + 1:
      # End of a continuous slot
      common_time_slots.append([
          minutes_to_time(slot_start),
          minutes_to_time(sorted_minutes[i - 1] + 1)
      ])
      slot_start = sorted_minutes[i]

  # Add the last slot
  common_time_slots.append(
      [minutes_to_time(slot_start),
       minutes_to_time(sorted_minutes[-1] + 1)])

  return common_time_slots


def FindGroupTimeSlots(thisdict):
  scheduledict = {}
  freetimesdict = {}
  endTimes = []
  startTimes = []
  duration_of_meeting = 30
  #O(n)
  for idx, name in enumerate(thisdict):
    if 'schedule' in name.lower():
      scheduledict[name.split('_')[0]] = thisdict[name]
      freetimesdict[name.split('_')[0]] = []
    if 'dailyact' in name.lower():
      endTimes.append(thisdict[name][1])
      startTimes.append(thisdict[name][0])
    if 'duration_of_meeting' in name.lower():
      duration_of_meeting = int(thisdict[name])
      if duration_of_meeting < 0:
        with open('Output.txt', 'a') as Wfile:
            Wfile.write("Error: Negative duration of meeting detected.")
            Wfile.write('\n--------------------\n')
        return
  if len(scheduledict) != len(freetimesdict):
    with open('Output.txt', 'a') as Wfile:
      Wfile.write("Person missing schedule or daily activity")
      Wfile.write('\n--------------------\n')
      return

  minOfEnd = endTimes[0]
  maxOfStart = startTimes[0]
  #O(n)
  for val in startTimes:
    if calculate_time_interval_manual(maxOfStart, val) > 0:
      maxOfStart = val
  for val in endTimes:
    if calculate_time_interval_manual(minOfEnd, val) < 0:
      minOfEnd = val
  prevVal = maxOfStart
  #O(n^2)
  for idx, name in enumerate(scheduledict):
    for idx2, val in enumerate(scheduledict[name]):

      if calculate_time_interval_manual(
          val[1], maxOfStart) < 0 and calculate_time_interval_manual(
              val[0], minOfEnd) > 0:
        if prevVal != val[0]:
          freetimesdict[name].append([prevVal, val[0]])  # [end, start2]
        prevVal = val[1]
        #print(freetimesdict)
      if calculate_time_interval_manual(val[1], minOfEnd) < 0:
        freetimesdict[name].append([prevVal, minOfEnd])
        prevVal = val[1]

      try:
        val = scheduledict[name][idx2 + 1]
      except:
        freetimesdict[name].append([prevVal, minOfEnd])

    prevVal = maxOfStart

    overlapping_slots = find_common_availability(freetimesdict)
  final_output_array = []
  #O(n)
  for idx, slot in enumerate(overlapping_slots):

    if calculate_time_interval_manual(slot[0], slot[1]) >= duration_of_meeting:
      final_output_array.append(slot)

  with open('Output.txt', 'a') as Wfile:
    Wfile.write(str(final_output_array))
    Wfile.write('\n--------------------\n')

  return


for x in arrayOfDict:
  FindGroupTimeSlots(x)
