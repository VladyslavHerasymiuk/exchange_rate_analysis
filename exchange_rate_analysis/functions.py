from lxml import html
import requests
import xml.etree.ElementTree as ET
import xml.dom.minidom
import eventlet
import sys


root = ET.Element('root')


def readBanksUrls(filename):
    filename = str(filename)
    try:
        tree = ET.parse(filename)
    except FileNotFoundError as e:
        print(e)
        return False
    else:
        root = tree.getroot()
        data = []
        for bank in root:
            for url in bank:
                data.append(url.text)
        return tuple(data)


def request_get(url):
    url = str(url)
    try:
        with eventlet.timeout.Timeout(10):
            response = requests.get(url)
            return response.text
    except requests.exceptions.ReadTimeout:
        print(("TIMED OUREADT -" + url))
        sys.exit()
    except requests.exceptions.ConnectionError:
        print("CONNECT ERROR -" + url)
        sys.exit()
    except eventlet.timeout.Timeout as e:
        print("TOTAL TIMEOUT -" + url)
        sys.exit()
    except requests.exceptions.RequestException as e:
        print("OTHER REQUESTS EXCEPTION -" + url + str(e))
        sys.exit()


def parse_rate_in_UniversalBank(text):
    results = {}
    tree = html.fromstring(text)
    xpath = '//table[@class="rate table ' \
            'table-bordered light fl-left' \
            ' m-t-0-xs m-t-sm-1"]/tbody/tr'
    table_tbody_tr = tree.xpath(xpath)[1:3]
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
    xpath_to_xml('Universal', xpath)
    return results


def parse_rate_in_OschadBank(text):
    results = {}
    tree = html.fromstring(text)
    xpath = '//span[@class="currency-rate"]'
    span_list = tree.xpath(xpath)[:2]
    it = iter(['USD', 'EUR'])

    for span in span_list:
        st = span.xpath('.//strong/text()')
        results.update({
            next(it): {
                'buy': st[0],
                'sell': st[1]
            }
        })
    xpath_to_xml('Oshad', xpath)
    return results


def parse_rate_in_PravexBank(text):
    results = {}
    tree = html.fromstring(text)
    xpath = '//div[@class="currency clearfix"]'
    table_tbody_tr = tree.xpath(xpath)[1:3]
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
    xpath_to_xml('Oshad', xpath)
    return results


def from_dict_to_xml(data):
    root = ET.Element('root')
    it_bank = iter(['Universal', 'Oschad', 'Pravex'])

    for bank in data:
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

    with open('static/Output.xml', 'w') as f:
        f.write(pretty_xml)


def xpath_to_xml(elname, xpath):
    global root
    el_name = ET.SubElement(root, elname)
    xp = ET.SubElement(el_name, 'xpath')
    xp.text = str(xpath)

    tree_out = ET.tostring(root, encoding="UTF-8")
    newXML = xml.dom.minidom.parseString(tree_out.decode('UTF-8'))
    pretty_xml = newXML.toprettyxml()

    with open('static/xpath.xml', 'w') as f:
        f.write(pretty_xml)


if __name__ == '__main__':
    rq_tuple = readBanksUrls('static/BanksUrls.xml')
    if rq_tuple:
        exchange_rate_data = (parse_rate_in_UniversalBank(
                            request_get(rq_tuple[0])),
                              parse_rate_in_OschadBank(
                            request_get(rq_tuple[1])),
                              parse_rate_in_PravexBank(
                            request_get(rq_tuple[2])))
        from_dict_to_xml(exchange_rate_data)
    exit()
    # json_data = [{'USD': {'buy': '26.45', 'sell': '26.80'},
    # 'EUR': {'buy': '32.55', 'sell': '33.05'}},
    # {'USD': {'buy': '26,1500', 'sell': '26,8000'},
    # 'EUR': {'buy': '32,0000', 'sell': '32,9000'}},
    # {'USD': {'buy': '26.3', 'sell': '26.6'},
    # 'EUR': {'buy': '32.4', 'sell': '32.9'}}]
