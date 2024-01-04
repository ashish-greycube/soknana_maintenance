import frappe
from frappe import ValidationError, _, msgprint
from frappe.utils.user import get_users_with_role
from frappe.utils  import cstr,cint


def fetch_approval_flags_from_item(self,method):
    parent_level_custom_om_approval_required=0
    parent_level_custom_deputy_om_approval_required=0
    for item in self.items:
        item.custom_om_approval_required=frappe.db.get_value('Item', item.item_code, 'custom_om_approval_required')
        if item.custom_om_approval_required==1:
            parent_level_custom_om_approval_required=1
        item.custom_deputy_om_approval_required=frappe.db.get_value('Item', item.item_code, 'custom_deputy_om_approval_required')
        if item.custom_deputy_om_approval_required==1:
            parent_level_custom_deputy_om_approval_required=1
    if parent_level_custom_om_approval_required==1:
        self.custom_om_approval_required=1
    if parent_level_custom_deputy_om_approval_required==1:
        self.custom_deputy_om_approval_required=1


# def update_material_status_on_cancel(self,method):
#     purchase_order=None
#     purchase_invoice=None
#     material_request=None
#     soknana_maintenance=None

#     if self.doctype=='Purchase Invoice':
#         for item in self.items:
#             if item.purchase_order:
#                 purchase_order=item.purchase_order
#                 exit
#         if purchase_order:
#             po = frappe.get_doc('Purchase Order', purchase_order)
#             for item in po.items:
#                 if item.material_request:
#                     material_request=item.material_request
#                     exit
#         if material_request:
#             soknana_maintenance=frappe.db.get_value('Material Request', material_request, 'custom_soknana_maintenance')
#         if soknana_maintenance:
#             frappe.db.set_value('Soknana Maintenance', soknana_maintenance, 'material_status', 'Ordered')     
#             frappe.msgprint(_("Soknana Maintenance {0} , material status is changed to <b>Ordered</b>").format(frappe.bold(soknana_maintenance)),alert=1,)     


def update_material_status(self,method):
    purchase_order=None
    purchase_invoice=None
    material_request=None
    soknana_maintenance=None

    if self.doctype=='Material Request':
        soknana_maintenance=frappe.db.get_value('Material Request', self.name, 'custom_soknana_maintenance')
        material_request=self.name
        if soknana_maintenance and (method=="on_submit" or method=="validate"):
            exisiting_material_status = frappe.db.get_value('Soknana Maintenance', soknana_maintenance, 'material_status')
            if exisiting_material_status!='Pending':
                frappe.db.set_value('Soknana Maintenance', soknana_maintenance, 'material_status', 'Pending')    
                frappe.msgprint(_("Soknana Maintenance {0} , material status is updated to <b>Pending</b>").format(frappe.bold(soknana_maintenance)),alert=1,)  
        elif soknana_maintenance and method=="on_cancel":
            frappe.db.set_value('Soknana Maintenance', soknana_maintenance, 'material_status', 'Not Applicable')     
            frappe.msgprint(_("Soknana Maintenance {0} , material status is changed to <b>Not Applicable</b>").format(frappe.bold(soknana_maintenance)),alert=1,)                       


    if self.doctype=='Purchase Order':
        for item in self.items:
            if item.material_request:
                material_request=item.material_request
                purchase_order=self.name
                exit
        if material_request:
            soknana_maintenance=frappe.db.get_value('Material Request', material_request, 'custom_soknana_maintenance')
            if soknana_maintenance and method=="on_submit":
                frappe.db.set_value('Soknana Maintenance', soknana_maintenance, 'material_status', 'Ordered')  
                frappe.msgprint(_("Soknana Maintenance {0} , material status is updated to <b>Ordered</b>").format(frappe.bold(soknana_maintenance)),alert=1,)   
            elif soknana_maintenance and method=="on_cancel":
                frappe.db.set_value('Soknana Maintenance', soknana_maintenance, 'material_status', 'Pending')     
                frappe.msgprint(_("Soknana Maintenance {0} , material status is changed to <b>Pending</b>").format(frappe.bold(soknana_maintenance)),alert=1,)                       


    if self.doctype=='Purchase Invoice':
        for item in self.items:
            if item.purchase_order:
                purchase_order=item.purchase_order
                exit
        if purchase_order:
            po = frappe.get_doc('Purchase Order', purchase_order)
            for item in po.items:
                if item.material_request:
                    material_request=item.material_request
                    exit
        if material_request:
            soknana_maintenance=frappe.db.get_value('Material Request', material_request, 'custom_soknana_maintenance')
        if soknana_maintenance and method=="on_submit":
            frappe.db.set_value('Soknana Maintenance', soknana_maintenance, 'material_status', 'Purchased')     
            frappe.msgprint(_("Soknana Maintenance {0} , material status is updated to <b>Purchased</b>").format(frappe.bold(soknana_maintenance)),alert=1,)                            
        elif soknana_maintenance and method=="on_cancel":
            frappe.db.set_value('Soknana Maintenance', soknana_maintenance, 'material_status', 'Ordered')     
            frappe.msgprint(_("Soknana Maintenance {0} , material status is changed to <b>Ordered</b>").format(frappe.bold(soknana_maintenance)),alert=1,)        

    # if self.doctype=='Purchase Invoice':
    #     for item in self.items:
    #         if item.purchase_order:
    #             purchase_order=item.purchase_order
    #             exit
    #     if purchase_order:
    #         po = frappe.get_doc('Purchase Order', purchase_order)
    #         for item in po.items:
    #             if item.material_request:
    #                 material_request=item.material_request
    #                 exit
    #     if material_request:
    #         soknana_maintenance=frappe.db.get_value('Material Request', material_request, 'custom_soknana_maintenance')
    #     if soknana_maintenance:
    #         frappe.db.set_value('Soknana Maintenance', soknana_maintenance, 'material_status', 'Purchased')


    # if self.doctype=='Purchase Order':
    #     for item in self.items:
    #             if item.material_request:
    #                 material_request=item.material_request
    #                 purchase_order=self.name
    #                 exit
    #     if material_request:
    #         soknana_maintenance=frappe.db.get_value('Material Request', material_request, 'custom_soknana_maintenance')
    #         if soknana_maintenance:
    #             pi=frappe.db.get_list('Purchase Invoice Item', filters={
    #                 'purchase_order': ['=', purchase_order]},
    #                 fields=['parent'],limit=1)            
    #             if len(pi)>0:
    #                 purchase_invoice=pi[0].parent
    #             if purchase_invoice:
    #                 frappe.db.set_value('Soknana Maintenance', soknana_maintenance, 'material_status', 'Purchased')
    #             else:     
    #                 frappe.db.set_value('Soknana Maintenance', soknana_maintenance, 'material_status', 'Ordered')    

    # if self.doctype=='Material Request':
    #     soknana_maintenance=frappe.db.get_value('Material Request', self.name, 'custom_soknana_maintenance')
    #     if soknana_maintenance:
    #         material_request=self.name
    #         po=frappe.db.get_list('Purchase Order Item', filters={
    #             'material_request': ['=', material_request]},
    #             fields=['parent'],limit=1)            
    #         if len(po)>0:
    #             purchase_order=po[0].parent  
    #         if purchase_order:
    #             pi=frappe.db.get_list('Purchase Invoice Item', filters={
    #                 'purchase_order': ['=', purchase_order]},
    #                 fields=['parent'],limit=1)            
    #             if len(pi)>0:
    #                 purchase_invoice=pi[0].parent
    #         if purchase_invoice:   
    #             frappe.db.set_value('Soknana Maintenance', soknana_maintenance, 'material_status', 'Purchased')  
    #         elif purchase_order:
    #             frappe.db.set_value('Soknana Maintenance', soknana_maintenance, 'material_status', 'Ordered') 
    #         elif material_request:
    #             frappe.db.set_value('Soknana Maintenance', soknana_maintenance, 'material_status', 'Pending')


                           
def validate_review_status(self,method):
    quality_supervisor_role = frappe.db.get_single_value('Soknana Settings', 'quality_supervisor_role')
    branch_manager_role = frappe.db.get_single_value('Soknana Settings', 'branch_manager_role')    
    # supervior_missing_attachment_idx=[]
    # branch_manager_missing_attachment_idx=[]

    if (frappe.session.user in get_users_with_role(quality_supervisor_role)) and (frappe.session.user not in get_users_with_role(branch_manager_role) or 'System Manager'):
        # for review in self.reviews:
        #     if review.status == 'Failed' and not review.custom_supervisor_review_attachment :
        #         supervior_missing_attachment_idx.append(cstr(review.idx))
        # if len(supervior_missing_attachment_idx)>0:
        #     print(supervior_missing_attachment_idx,'supervior_missing_attachment_idx')
        #     supervior_missing_attachment_idx_string=','.join(supervior_missing_attachment_idx)
        #     frappe.throw(title='Error', msg='Please provide supervisor review attahcment for row {0}. This is required when quality supervisor marks review as failed.'.
        #                      format(frappe.bold(supervior_missing_attachment_idx_string)),) 

        for review in self.reviews:
            if review.status == 'Failed' and not review.custom_supervisor_review_attachment :
                frappe.throw(title='Error', msg='Please provide supervisor review attahcment for row {0}. This is required when quality supervisor marks review as failed.'.
                                format(frappe.bold(review.idx)),)                
            if review.custom_supervisor_status == 'Passed' or review.custom_supervisor_status == 'Failed':
                frappe.throw(title='Error', msg='User {0} having role {1} is allowed to change status only once.<br> Please contact branch manager role user for futher changes'.
                             format(frappe.bold(frappe.session.user),frappe.bold(quality_supervisor_role)),)
            else:    
                review.custom_supervisor_status=review.status


    if (frappe.session.user  in get_users_with_role(branch_manager_role)):
        for review in self.reviews:
            if review.custom_supervisor_status!=review.status and review.custom_supervisor_status=='Failed' and review.custom_review_attachment==None:
                frappe.throw(title='Error', msg='Please provide review attahcment for row {0}. This is required as quality supervisor has failed it earlier.'.
                             format(frappe.bold(review.idx)),)                


def calculate_success_rate(self,method):
    passed_target_total=0
    all_target_total=0
    for review in self.reviews:
        all_target_total=all_target_total+cint(review.target)
        if review.custom_supervisor_status=='Passed':
            passed_target_total=passed_target_total+cint(review.target)
    self.custom_success_rate=(passed_target_total/all_target_total)*100


def check_picture_required_for_purchase_receipt(self,method):
    for row_item in self.items:
        custom_required_picture_in_receipt_cf = frappe.db.get_value('Item', row_item.item_code, 'custom_required_picture_in_receipt_cf')
        if custom_required_picture_in_receipt_cf==1 and self.custom_product_picture_cf==None:
            frappe.throw(
                title='Attachment Missing',
                msg='Row: {0} : Item {1} requires picture attachment. Please provide to proceed...'.format(row_item.idx,row_item.item_name))            


