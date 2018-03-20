from lxml import html
import requests
import xml.etree.ElementTree as ET
import xml.dom.minidom


def request_get(url):
    r = requests.get(url)
    return r.text


def parse_rate_in_UniversalBank(text):
    results = {}
    tree = html.fromstring(text)
    table_tbody_tr = tree.xpath('//table[@class="rate table '
                                'table-bordered light fl-left'
                                ' m-t-0-xs m-t-sm-1"]/tbody/tr')[1:3]
    it = iter(['USD', 'EUR'])

    for tr_val in table_tbody_tr:
        td = tr_val.xpath('.//td/text()')[1:3]
        td = list(map(lambda x: "".join(x.split()), td))
        results.update({
                next(it): {
                    'buy': td[0],
                    'sell': td[1]
                }
            })
    return results


def parse_rate_in_OschadBank(text):
    results = {}
    tree = html.fromstring(text)
    span_list = tree.xpath('//span[@class="currency-rate"]')[:2]
    it = iter(['USD', 'EUR'])

    for span in span_list:
        st = span.xpath('.//strong/text()')
        results.update({
            next(it): {
                'buy': st[0],
                'sell': st[1]
            }
        })
    return results


def parse_rate_in_PravexBank(text):
    results = {}
    tree = html.fromstring(text)
    table_tbody_tr = tree.xpath('//div[@class="currency clearfix"]')[1:3]
    it = iter(['USD', 'EUR'])

    for tr_val in table_tbody_tr:
        td = tr_val.xpath('.//div/text()')[2::2]
        td = list(map(lambda x: "".join(x.split()), td))
        results.update({
            next(it): {
                'buy': td[0],
                'sell': td[1]
            }
        })
    return results


if __name__ == '__main__':
    universalUrl = 'https://www.universalbank.com.ua/'
    oschadUrl = 'https://www.oschadbank.ua/'
    pravexUrl = 'https://www.pravex.com.ua/'

    json_data = [parse_rate_in_UniversalBank(request_get(universalUrl)),
                 parse_rate_in_OschadBank(request_get(oschadUrl)),
                 parse_rate_in_PravexBank(request_get(pravexUrl))]

    # json_data = [{'USD': {'buy': '26.45', 'sell': '26.80'},
    # 'EUR': {'buy': '32.55', 'sell': '33.05'}},
    # {'USD': {'buy': '26,1500', 'sell': '26,8000'},
    # 'EUR': {'buy': '32,0000', 'sell': '32,9000'}},
    # {'USD': {'buy': '26.3', 'sell': '26.6'},
    # 'EUR': {'buy': '32.4', 'sell': '32.9'}}]

    root = ET.Element('root')
    it_bank = iter(['Universal', 'Oschad', 'Pravex'])

    for bank in json_data:
        bank_name = ET.SubElement(root, next(it_bank))

        for r in ['USD', 'EUR']:
            rate = ET.SubElement(bank_name, r)
            buy = ET.SubElement(rate, 'buy')
            sell = ET.SubElement(rate, 'sell')

            buy.text = bank[r]['buy']
            sell.text = bank[r]['sell']

    tree_out = ET.tostring(root, encoding="UTF-8")
    newXML = xml.dom.minidom.parseString(tree_out.decode('UTF-8'))
    pretty_xml = newXML.toprettyxml()

    with open('Output.xml', 'w') as f:
        f.write(pretty_xml)
