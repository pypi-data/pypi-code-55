yn_ques_map = {
    "yes": ["হ্যাঁ","হ্যা","জ্বী", "খেয়েছি", "খাইছি", "খেয়েছিলাম","আচ্ছা", "আছে", "আছেতো", "অনেক আছে", "অনেক", "আছে", "অল্প আছে", "ইয়েস", "হুম", "হ", "হু", "hm", "hum", "hu", "yes", "চাই", "চায়", "চাচ্ছি", "সিউর", "sure", "ওকে", "অকে", "oka", "ok", "okay", "একটু", "মোটামুটি","অল্প", "কিছুটা", "মোটামোটি","অনেক", "বেশি", "সামান্য", "কিছু", "হালকা"],
    "no" : ["না", "নাই", "একদম নাই", "নাইতো", "ছিলো", "ছিল" ,"এখন নাই", "নেই", "নেইতো", "ছিলোত", "নো", "ন", "নানা", "no", "na", "never", "নেভার", "নেবার", "খাইনি ", "চাইনা", "চায়না", "হয়নি", "নাতো","হয়না", "খাইনি"],
    "male" : ["পুরুষ", "মেইল", "মেল", "মরদ ফুয়া", "ছেলে", "পুলা", "পোয়া", "পোলা", "মদ্দা", "নর", "বাবা", "মামা", "চাচা", "ছাত্র", "পুত", "male", "boy", "বয়", "বাপ", "আব্বা" ],
    "female" : ["ফিমেল", "মহিলা", "মাইয়া", "মেয়ে", "লেরকি", "নারী", "ছাত্রী", "আন্টি", "মামি", "মা", "ভাবী", "বোদি", "বেটী", "বেটি", "অন্যান্য", "other", "আদারস", "female", "হিজড়া", "জানিনা", "গার্ল", "girl", "গাল"]
}
	
bangla_number = ['০', '১','২', '৩','৪',
                 '৫','৬', '৭', '৮', '৯']

english_number = ['0', '1', '2', '3', '4',
                  '5', '6', '7', '8', '9']
def BTE(original):
    converted = ""
    for character in str(original):
        if character in bangla_number:
            converted+=english_number[bangla_number.index(character)]
        else:
            converted+=character
    return converted
	
def convert(ind, text):
  if ind == 0 or ind ==3:
    text = BTE(text)
    age_temp = [int(s) for s in text.split() if s.isdigit()]

    if len(age_temp)==1:
      return str(age_temp[0])
    else: return 'sdk'

  elif ind == 1:
    gen_male = sum([s in i.split() for s in text.split() for i in yn_ques_map["male"]])
    gen_female = sum([s in i.split() for s in text.split() for i in yn_ques_map["female"]])
    if gen_male:
      return "tdk"
    elif gen_female:
      return "fdk"
    else: return 'sdk'

  else:
    y_val = sum([s in i.split() for s in text.lower().split() for i in yn_ques_map["yes"]])
    n_val = sum([s in i.split() for s in text.lower().split() for i in yn_ques_map["no"]])
    if y_val >  n_val:
        return "tdk"
    elif y_val <  n_val:
        return "fdk"
    else: return 'sdk'



 