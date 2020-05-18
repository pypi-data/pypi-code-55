import json, os
import csv
import xlsxwriter
# import pdfkit

class Output:
    
    def __init__(self, data): 
        self.data = data
    
    def convert_to_json(self):
        file_path = os.getcwd()
        result = list(filter(lambda rule: rule['result'] != 'success', self.data)) 
        json_object = json.dumps(result, indent = 4)
        file_path = "".join([file_path, "/aws-audit-report.json"])
        with open(file_path, 'w') as outfile:
            outfile.write(json_object) 
        
        return file_path

    def convert_to_excel(self):
        
        # Get file path for excel file to store
        file_path = os.getcwd()
        file_path = "".join([file_path, "/aws-audit-report.xlsx"])

        # Initializing Working instance
        workbook = xlsxwriter.Workbook(file_path)

        # Creating working formats
        header_format = workbook.add_format({'bg_color': '#2F4F4F', 'border': 1, 'align': 'left', 'valign': 'top', 'font_color': '#FFFFFF', 'bold': True})
        severity_high = workbook.add_format({'bg_color': '#FF0000', 'border': 1, 'font_color': '#FFFFFF', 'bold': True, 'text_wrap': True, 'align': 'center', 'valign': 'vcenter'})
        severity_medium = workbook.add_format({'bg_color': '#FF8C00', 'border': 1, 'font_color': '#FFFFFF', 'bold': True, 'text_wrap': True, 'align': 'center', 'valign': 'vcenter'})
        severity_low = workbook.add_format({'bg_color': '#FFD700', 'border': 1, 'font_color': '#FFFFFF', 'bold': True, 'text_wrap': True, 'align': 'center', 'valign': 'vcenter'})
        # rule_header_format = workbook.add_format({'bold': True, 'border': 1, 'align': 'left', 'valign': 'top'})
        generic_format = workbook.add_format({'border': 1, 'align': 'left', 'valign': 'top', 'text_wrap': True})
        merge_format = workbook.add_format({'bold': 1, 'border': 1, 'align': 'center', 'valign': 'vcenter'})

        # Initializing headers array
        service_headers = ['Service', 'Rule ID', "Issue", "Severity", "Resolution"]
        rule_headers = ['Region', 'Resource Name', 'Resource ARN', 'Type', 'Message (If Any)']

        previous_service = ""
        row = 2

        for rule in self.data:

            # Creating new worksheet for each service if any failed rules are their
            if previous_service != rule['service'] and rule['result'] == 'failure':
                worksheet = workbook.add_worksheet(rule['service'])
                worksheet.set_column(1, 1, 15)
                worksheet.set_column(2, 2, 20)
                worksheet.set_column(3, 3, 60)
                worksheet.set_column(4, 4, 15)
                worksheet.set_column(5, 5, 70)

                row = 2
            
            # Add only failed rules for worksheet
            if rule['result'] == 'failure':
                col = 1
                for header in service_headers:
                    worksheet.write(row, col, header, header_format)
                    col = col + 1
                
                row = row +  1

                worksheet.write(row, 1, rule['service'], generic_format)    
                worksheet.write(row, 2, rule['id'], generic_format)
                worksheet.write(row, 3, rule['issue'], generic_format)
                if rule['severity'] == 'high':
                    worksheet.write(row, 4, rule['severity'].capitalize(), severity_high)
                elif rule['severity'] == 'medium':
                    worksheet.write(row, 4, rule['severity'].capitalize(), severity_medium)
                elif rule['severity'] == 'low':
                    worksheet.write(row, 4, rule['severity'].capitalize(), severity_low)

                worksheet.write(row, 5, rule['resolution'], generic_format)

                row = row + 1

                worksheet.merge_range(row, 1, row, 5, 'Failed Resources', merge_format)

                row = row + 1 
       
                col = 1
                for header in rule_headers:
                    worksheet.write(row, col, header, header_format)
                    col = col + 1
                
                for data in rule['data']:
                    row = row + 1
                    
                    worksheet.write(row, 1, data.get('region', ''), generic_format)    
                    worksheet.write(row, 2, data.get('name', ''), generic_format)
                    worksheet.write(row, 3, data.get('arn', ''), generic_format)            
                    worksheet.write(row, 4, data.get('type', ''), generic_format)            
                    worksheet.write(row, 5, data.get('message', ''), generic_format)

                row = row + 3

                previous_service = rule['service']

        workbook.close()

        return file_path
         
    # def convert_to_pdf(self):
    #     previous_service = ""
    #     service_headers = ['Service', 'Rule ID', "Issue", "Severity", "Resolution"]
    #     rule_headers = ['Region', 'Resource Name', 'Resource ARN', 'Type', 'Message (If Any)']
    #     json_context = {}

    #     # Creating context JSON for creating HTML string
    #     for rule in self.data:

    #         if previous_service != rule['service'] and rule['result'] == 'failure':
    #             json_context[rule['service']] = {}

    #         if rule['result'] == 'failure':
    #             json_context[rule['service']]
    #             rule_info = {}
    #             # Create rule_info JSON
    #             for header in service_headers:
    #                 rule_info = {
    #                                 'Service': rule['service'],
    #                                 'Rule ID': rule['id'],
    #                                 'Issue': rule['issue'],
    #                                 'Severity': rule['severity'],
    #                                 'Resolution': rule['resolution']
    #                             }

    #             # Create failures LIST for rule
    #             failures = []
    #             for data in rule['data']:
    #                 failures.append({
    #                                 'Region': data.get('region', ''),
    #                                 'Resource Name': data.get('name', ''),
    #                                 'Resource ARN': data.get('arn', ''),
    #                                 'Type': data.get('type', ''),
    #                                 'Message (If Any)': data.get('message', ''),
    #                                 })
                
    #             if rule['id'] not in json_context[rule['service']]:
    #                 json_context[rule['service']][rule['id']] = {'rule_info': rule_info, 'failures': failures}
                
    #             previous_service = rule['service']

    #     html = '''
    #             <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
    #             <html>
    #             <head>
    #                 <meta http-equiv="content-type" content="text/html; charset=utf-8"/>
    #                 <title></title>
    #                 <style type="text/css">
    #                     body,div,table,thead,tbody,tfoot,tr,th,td,p { font-family:"Arial"; font-size:x-small; page-break-inside: avoid !important;}
    #                     a.comment-indicator:hover + comment { background:#ffd; position:absolute; display:block; border:1px solid black; padding:0.5em;  } 
    #                     a.comment-indicator { background:red; display:inline-block; border:1px solid black; width:0.5em; height:0.5em;  } 
    #                     comment { display:none;  } 
    #                     .header{padding: 4px; height: 20px; text-align: left; vertical-align: top; background-color: #2F4F4F; color:#FFFFFF; font-weight: bold; border: 1px solid #000000;}
    #                     .data{height: 20px; text-align: left; vertical-align: color:#000000; border: 1px solid #000000;}
    #                     .merge{height: 20px; text-align: center; color:#000000; font-weight: bold; border: 1px solid #000000;}
    #                     .space{height: 20px;}
    #                     .red{text-transform: uppercase;background-color: red;}
    #                     .orange{text-transform: uppercase;background-color: orange;}
    #                     .yello{text-transform: uppercase;background-color: yellow;}
    #                     @media print {.new-page {page-break-before: always;}}
    #                 </style>
    #             </head>
    #             <body>
    #             <table cellspacing="0" border="0">
    #             '''
    #     processed_rules = []
    #     processed_services = []
    #     space = '<tr><td class="space" colspan=5></td></tr>'
    #     merge_tr = '<tr><td class="merge" colspan=5>Failed Resources</td></tr>'
    #     for service, service_data in json_context.items():
    #         if service not in processed_services:
    #             processed_services.append(service)
    #         service_html = ''
    #         for rule_id, rule_data in service_data.items():
    #             rule_html = ''
    #             if rule not in processed_rules:
    #                 processed_rules.append(rule_id)
    #                 head_tr = '<tr>'
    #                 data_tr = '<tr>'

    #                 for key, value in rule_data['rule_info'].items():
    #                     head_tr += f'<td class="header">{key}</td>'
    #                     severity = ''
    #                     if key == 'Severity':
    #                         severity = 'red' if value == 'high' else ('orange' if value == 'medium' else 'yellow')
    #                     data_tr += f'<td class="data {severity}">{value}</td>'
    #                 head_tr += '</tr>'
    #                 data_tr += '</tr>'
                    
    #                 rule_html += head_tr + data_tr + merge_tr
                
    #             head_tr = '<tr>'
    #             failure_head = True
    #             for failure in rule_data['failures']:
    #                 if failure_head:
    #                     failure_head = False
    #                     for key in failure.keys():
    #                         head_tr += f'<td class="header">{key}</td>'
    #                     rule_html += head_tr 
                        
    #                 data_tr = '<tr>'
    #                 for value in failure.values():
    #                     data_tr += f'<td class="data">{value}</td>'
    #                 data_tr += '</tr>'
    #                 rule_html += data_tr
                
    #             rule_html += str(space * 2)
    #             service_html += rule_html
    #             # print(service_html)
    #         html += service_html

    #     html += '</table></body></html>'

    #     file_path = os.getcwd()
    #     file_path = ''.join([file_path, '/testpdf.pdf'])
    #     pdfkit.from_string(html,file_path)

    #     return file_path
