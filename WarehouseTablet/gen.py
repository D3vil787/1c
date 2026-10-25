import uuid, os, re, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = sys.argv[1]
shutil.rmtree(OUT, ignore_errors=True)
src = open(ROOT + '/MinStockNotify/Configuration.xml', encoding='utf-8-sig').read()
head = src[:src.index('<Configuration ')]
import random
R = random.Random(20261002)
u = lambda: str(uuid.UUID(int=R.getrandbits(128), version=4))
def w(path, text, bom=True):
    p = os.path.join(OUT, path); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8-sig' if bom else 'utf-8', newline='\n').write(text)
def syn(t): return '<Synonym>\n\t\t\t\t<v8:item>\n\t\t\t\t\t<v8:lang>ru</v8:lang>\n\t\t\t\t\t<v8:content>%s</v8:content>\n\t\t\t\t</v8:item>\n\t\t\t</Synonym>' % t
# Configuration
cls = ['9cd510cd-abfc-11d4-9434-004095e12fc7','9fcd25a0-4822-11d4-9414-008048da11f9','e3687481-0a87-462c-a166-9f34594f9bba','9de14907-ec23-4a07-96f0-85521cb6b53b','51f2d5d8-ea4d-4064-8892-82951750031e','e68182ea-4237-4383-967f-90c1e3370bc7','fb282519-d103-4dd3-bc12-cb271d631dfc']
ci = ''.join('\t\t\t<xr:ContainedObject>\n\t\t\t\t<xr:ClassId>%s</xr:ClassId>\n\t\t\t\t<xr:ObjectId>%s</xr:ObjectId>\n\t\t\t</xr:ContainedObject>\n' % (c, u()) for c in cls)
cfg = head + '''<Configuration uuid="%s">
		<InternalInfo>
%s		</InternalInfo>
		<Properties>
			<ObjectBelonging>Adopted</ObjectBelonging>
			<Name>WarehouseTablet</Name>
			<Synonym>
				<v8:item>
					<v8:lang>ru</v8:lang>
					<v8:content>Склад: планшет (перемещение по штрихкоду)</v8:content>
				</v8:item>
			</Synonym>
			<Comment/>
			<ConfigurationExtensionPurpose>Customization</ConfigurationExtensionPurpose>
			<KeepMappingToExtendedConfigurationObjectsByIDs>true</KeepMappingToExtendedConfigurationObjectsByIDs>
			<NamePrefix>Планшет_</NamePrefix>
			<ConfigurationExtensionCompatibilityMode>Version8_3_24</ConfigurationExtensionCompatibilityMode>
			<DefaultRunMode>ManagedApplication</DefaultRunMode>
			<UsePurposes>
				<v8:Value xsi:type="app:ApplicationUsePurpose">PlatformApplication</v8:Value>
			</UsePurposes>
			<ScriptVariant>Russian</ScriptVariant>
			<DefaultRoles/>
			<Vendor/>
			<Version/>
			<DefaultLanguage>Language.Русский</DefaultLanguage>
			<BriefInformation/>
			<DetailedInformation/>
			<Copyright/>
			<VendorInformationAddress/>
			<ConfigurationInformationAddress/>
			<InterfaceCompatibilityMode>Taxi</InterfaceCompatibilityMode>
		</Properties>
		<ChildObjects>
			<Language>Русский</Language>
			<CommonModule>СкладПланшетСервер</CommonModule>
%s			<Role>СкладПланшет</Role>
			<HTTPService>СкладПланшет</HTTPService>
		</ChildObjects>
	</Configuration>
</MetaDataObject>''' % (u(), ci, ('\t\t\t<CommonModule>СкладПланшетТест</CommonModule>\n' if os.environ.get('TEST') else ''))
w('Configuration.xml', cfg)
lang = open(ROOT + '/MinStockNotify/Languages/Русский.xml', encoding='utf-8-sig').read()
lang = re.sub(r'<Language uuid="[^"]*"', '<Language uuid="%s"' % u(), lang)
w('Languages/Русский.xml', lang)
# Common module
cm = open(ROOT + '/MinStockNotify/CommonModules/МинОстаткиУведомления.xml', encoding='utf-8-sig').read()
cm = re.sub(r'<CommonModule uuid="[^"]*"', '<CommonModule uuid="%s"' % u(), cm)
cm = cm.replace('МинОстаткиУведомления', 'СкладПланшетСервер').replace('Уведомления о минимальном остатке', 'Склад-планшет: серверная логика')
cm = cm.replace('<ExternalConnection>false', '<ExternalConnection>true')
w('CommonModules/СкладПланшетСервер.xml', cm)
w('CommonModules/СкладПланшетСервер/Ext/Module.bsl', open(HERE + '/src/Module.bsl', encoding='utf-8').read())
if os.environ.get('TEST'):
    t = re.sub(r'<CommonModule uuid="[^"]*"', '<CommonModule uuid="%s"' % uuid.uuid4(), cm).replace('СкладПланшетСервер', 'СкладПланшетТест')
    w('CommonModules/СкладПланшетТест.xml', t)
    w('CommonModules/СкладПланшетТест/Ext/Module.bsl', open(HERE + '/src/TestModule.bsl', encoding='utf-8').read())
# HTTP service
def method(n, http, h):
    return '''<Method uuid="%s">
						<Properties>
							<Name>%s</Name>
							<Synonym>
								<v8:item>
									<v8:lang>ru</v8:lang>
									<v8:content>%s</v8:content>
								</v8:item>
							</Synonym>
							<Comment/>
							<HTTPMethod>%s</HTTPMethod>
							<Handler>%s</Handler>
						</Properties>
					</Method>''' % (u(), n, n, http, h)
def tmpl(n, t, methods):
    return '''<URLTemplate uuid="%s">
				<Properties>
					<Name>%s</Name>
					<Synonym>
						<v8:item>
							<v8:lang>ru</v8:lang>
							<v8:content>%s</v8:content>
						</v8:item>
					</Synonym>
					<Comment/>
					<Template>%s</Template>
				</Properties>
				<ChildObjects>
					%s
				</ChildObjects>
			</URLTemplate>''' % (u(), n, n, t, '\n\t\t\t\t\t'.join(methods))
hs = head + '''<HTTPService uuid="%s">
		<Properties>
			<Name>СкладПланшет</Name>
			%s
			<Comment/>
			<RootURL>sklad</RootURL>
			<ReuseSessions>AutoUse</ReuseSessions>
			<SessionMaxAge>900</SessionMaxAge>
		</Properties>
		<ChildObjects>
			%s
			%s
		</ChildObjects>
	</HTTPService>
</MetaDataObject>''' % (u(), syn('Склад: планшет'),
    tmpl('Страница', '/page', [method('GET', 'GET', 'СтраницаGET')]),
    tmpl('Данные', '/api/{Действие}', [method('GET', 'GET', 'ДанныеGET'), method('POST', 'POST', 'ДанныеPOST')]))
w('HTTPServices/СкладПланшет.xml', hs)
# page chunks
html = open(HERE + '/src/page.html', encoding='utf-8').read().replace('\r', '').split('\n')
chunks = []
for i in range(0, len(html), 40):
    part = html[i:i+40]
    lines = [l.replace('"', '""') for l in part]
    chunks.append('\tЧасти.Добавить(\n\t"' + '\n\t|'.join(lines) + '");')
lib = open(HERE + '/vendor/html5-qrcode.min.js', encoding='utf-8').read().replace('\r', '')
assert '\n' not in lib.strip('\n')
lib = lib.strip('\n')
LIBCHUNKS = '\n'.join('\tЧасти.Добавить("' + lib[i:i+2500].replace('"', '""') + '");' for i in range(0, len(lib), 2500))
bsl = '''#Область ОбработчикиСобытий

Функция СтраницаGET(Запрос)
	Ответ = Новый HTTPСервисОтвет(200);
	Ответ.Заголовки.Вставить("Content-Type", "text/html; charset=utf-8");
	Ответ.Заголовки.Вставить("Cache-Control", "no-store");
	Ответ.УстановитьТелоИзСтроки(ТекстСтраницы(), КодировкаТекста.UTF8, ИспользованиеByteOrderMark.НеИспользовать);
	Возврат Ответ;
КонецФункции

Функция ДанныеGET(Запрос)
	Если Запрос.ПараметрыURL["Действие"] = "lib" Тогда
		Ответ = Новый HTTPСервисОтвет(200);
		Ответ.Заголовки.Вставить("Content-Type", "application/javascript; charset=utf-8");
		Ответ.Заголовки.Вставить("Cache-Control", "public, max-age=86400");
		Ответ.УстановитьТелоИзСтроки(ТекстБиблиотеки(), КодировкаТекста.UTF8, ИспользованиеByteOrderMark.НеИспользовать);
		Возврат Ответ;
	КонецЕсли;
	Возврат ОтветДанных(Запрос);
КонецФункции

Функция ДанныеPOST(Запрос)
	Возврат ОтветДанных(Запрос);
КонецФункции

#КонецОбласти

#Область Служебные

Функция ОтветДанных(Запрос)
	Действие = Запрос.ПараметрыURL["Действие"];
	Попытка
		Если Действие = "init" Тогда
			Тело = СкладПланшетСервер.Инициализация();
		ИначеЕсли Действие = "scan" Тогда
			Тело = СкладПланшетСервер.Скан(Запрос.ПолучитьТелоКакСтроку("UTF-8"));
		ИначеЕсли Действие = "move" Тогда
			Тело = СкладПланшетСервер.Переместить(Запрос.ПолучитьТелоКакСтроку("UTF-8"));
		ИначеЕсли Действие = "iload" Тогда
			Тело = СкладПланшетСервер.ИнвЗагрузить(Запрос.ПолучитьТелоКакСтроку("UTF-8"));
		ИначеЕсли Действие = "iscan" Тогда
			Тело = СкладПланшетСервер.ИнвСкан(Запрос.ПолучитьТелоКакСтроку("UTF-8"));
		ИначеЕсли Действие = "isave" Тогда
			Тело = СкладПланшетСервер.ИнвСохранить(Запрос.ПолучитьТелоКакСтроку("UTF-8"));
		ИначеЕсли Действие = "asearch" Тогда
			Тело = СкладПланшетСервер.ПоискНоменклатуры(Запрос.ПолучитьТелоКакСтроку("UTF-8"));
		ИначеЕсли Действие = "aadd" Тогда
			Тело = СкладПланшетСервер.ДобавитьПоступление(Запрос.ПолучитьТелоКакСтроку("UTF-8"));
		ИначеЕсли Действие = "aprint" Тогда
			Тело = СкладПланшетСервер.ПечатьШтрихкода(Запрос.ПолучитьТелоКакСтроку("UTF-8"));
		Иначе
			Тело = "{""ok"":false,""error"":""Неизвестное действие""}";
		КонецЕсли;
	Исключение
		Текст = СтрЗаменить(КраткоеПредставлениеОшибки(ИнформацияОбОшибке()), """", "'");
		Текст = СтрЗаменить(СтрЗаменить(Текст, Символы.ПС, " "), "\\", "/");
		Тело = "{""ok"":false,""error"":""Ошибка сервера: " + Текст + """}";
	КонецПопытки;
	Ответ = Новый HTTPСервисОтвет(200);
	Ответ.Заголовки.Вставить("Content-Type", "application/json; charset=utf-8");
	Ответ.Заголовки.Вставить("Cache-Control", "no-store");
	Ответ.УстановитьТелоИзСтроки(Тело, КодировкаТекста.UTF8, ИспользованиеByteOrderMark.НеИспользовать);
	Возврат Ответ;
КонецФункции

Функция ТекстСтраницы()
	Части = Новый Массив;
''' + '\n'.join(chunks) + '''
	Возврат СтрСоединить(Части, Символы.ПС);
КонецФункции

// Библиотека распознавания штрихкодов камерой (html5-qrcode, Apache-2.0), отдается страницей по запросу.
Функция ТекстБиблиотеки()
	Части = Новый Массив;
''' + LIBCHUNKS + '''
	Возврат СтрСоединить(Части, "");
КонецФункции

#КонецОбласти
'''
w('HTTPServices/СкладПланшет/Ext/Module.bsl', bsl)
# Role
role = head + '''<Role uuid="%s">
		<Properties>
			<Name>СкладПланшет</Name>
			%s
			<Comment/>
		</Properties>
	</Role>
</MetaDataObject>''' % (u(), syn('Склад: планшет (доступ к HTTP-сервису)'))
w('Roles/СкладПланшет.xml', role)
objs = ''.join('\t<object>\n\t\t<name>HTTPService.СкладПланшет.URLTemplate.%s.Method.%s</name>\n\t\t<right>\n\t\t\t<name>Use</name>\n\t\t\t<value>true</value>\n\t\t</right>\n\t</object>\n' % (t, m) for t, m in [('Страница','GET'),('Данные','GET'),('Данные','POST')])
rights = '''<?xml version="1.0" encoding="UTF-8"?>
<Rights xmlns="http://v8.1c.ru/8.2/roles" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="Rights" version="2.20">
	<setForNewObjects>false</setForNewObjects>
	<setForAttributesByDefault>true</setForAttributesByDefault>
	<independentRightsOfChildObjects>false</independentRightsOfChildObjects>
''' + objs + '</Rights>'
w('Roles/СкладПланшет/Ext/Rights.xml', rights)
print('built', OUT)
