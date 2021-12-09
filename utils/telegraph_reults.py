import asyncio
from pprint import pprint
from telegraph import Telegraph 
# async def main():
    
telegraph = Telegraph()
print(telegraph.create_account(short_name='Bobir_Mardonov', author_name='Bobir Mardonov', author_url="http://t.me/Bobir_Mardonov"))

response = telegraph.create_page('Test 15 natijalari ',html_content='<p>Qatnashuvchilar reytingi</p>')
urls = response
for n in enumerate(urls):
    print(n)
print(urls['url'])
# asyncio.run(main())