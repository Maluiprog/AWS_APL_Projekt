import boto3
import streamlit as st
import datetime

AWS_REGION = "us-east-1"  # Ändra detta till din önskade region, t.ex. "eu-west-1" för Irland
# Skapa en DynamoDB-resurs med specificerad region
dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)

table = dynamodb.Table("inlagg")
today = datetime.datetime.today()
week_num = today.isocalendar()[1]
formatted_datetime = today.strftime("%Y-%m-%d %H:%M")



def add_entry(title, content, mood,week_num, formatted_datetime):
    table.put_item(
        Item={
            'week': week_num,
            'timestamp': formatted_datetime,
            'title': title,
            'content': content,
            'mood': mood
        }
    )


def get_entries_by_week(week):
    response = table.scan(
        FilterExpression=boto3.dynamodb.conditions.Attr('week').eq(week)
    )
    return response['Items']

st.title('APL-veckorapport')
st.subheader('Lägg till inlägg')
st.write('Fyll i formuläret nedan för att lägga till ett nytt inlägg')
title = st.text_input('Titel')
content = st.text_area(f'Innehåll vecka {week_num}')
mood = st.selectbox('Humör', ["😀", "😭", '😠', '😕', '😐'])
if st.button('Lägg till'):
    if not title or not content:
        st.error('Titel och innehåll är obligatoriska')
    else:
        add_entry(title, content, mood, week_num, formatted_datetime)
        st.success('Inlägg tillagt!')


def huvudsida():
    st.subheader('Se inlägg')

    # Skapa en lista med tillåtna veckor (38-49, exklusive 44)
    allowed_weeks = [str(week) for week in range(38, 50) if week != 44]
    selected_week = st.selectbox("Välj vecka att visa", allowed_weeks)

    items = get_entries_by_week(int(selected_week))

    if not items:
        st.info(f"Inga inlägg hittades för vecka {selected_week}.")
    else:
        for item in items:
            st.write(f"**Vecka:** {item['week']}")
            st.write(f"**Datum:** {item['timestamp']}")
            st.write(f"**Titel:** {item['title']}")
            st.write(f"**Innehåll:** {item['content']}")
            st.write(f"**Humör:** {item['mood']}")
            st.write('---')


def main():
    #sidebarstart()
    huvudsida()


if __name__ == "__main__":
    main()
