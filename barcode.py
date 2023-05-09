import cv2
import time
import openfoodfacts
from PIL import Image
from pyzbar.pyzbar import decode

unwanted_keys = ['vitamins_tags', 'vitamins_prev_tags', 'update_key', 'unknown_nutrients_tags', 'unknown_ingredients_n', 'unique_scans_n', 'traces_tags', 'traces_lc', 'traces_hierarchy', 'traces_from_user', 'traces_from_ingredients', 'traces', 'stores_tags', 'stores', 'states_tags', 'states_hierarchy', 'states', 'sortkey', 'selected_images', 'scans_n', 'rev', 'removed_countries_tags', 'quantity', 'purchase_places_tags', 'purchase_places', 'product_quantity', 'product_name_nl', 'popularity_tags', 'popularity_key', 'pnns_groups_2_tags', 'pnns_groups_2', 'pnns_groups_1_tags', 'pnns_groups_1', 'photographers_tags', 'packagings', 'packaging_tags', 'packaging_old', 'packaging_lc', 'packaging_hierarchy', 'packaging', 'other_nutritional_substances_tags', 'other_nutritional_substances_prev_tags', 'origins_tags', 'origins_old', 'origins_hierarchy', 'origins_lc', 'origins', 'nutrition_score_warning_fruits_vegetables_nuts_estimate_from_ingredients_value', 'nutrition_score_warning_fruits_vegetables_nuts_estimate_from_ingredients', 'nutrition_score_debug', 'nutrition_score_beverage', 'nutrition_grades_tags', 'nutrition_grades', 'nutrition_grade_fr', 'nutrition_data_prepared_per', 'nutrition_data_per', 'nutriscore_score_opposite', 'nutriscore_score', 'nutriscore_grade', 'nutrient_levels_tags', 'nucleotides_tags', 'nucleotides_prev_tags', 'nova_groups_tags', 'nova_groups_markers', 'nova_groups', 'nova_group_debug', 'nova_group', 'no_nutrition_data', 'misc_tags', 'minerals_tags', 'minerals_prev_tags', 'max_imgid', 'manufacturing_places_tags', 'manufacturing_places', 'main_countries_tags', 'link', 'lc', 'last_modified_t', 'last_modified_by', 'last_image_t', 'last_image_dates_tags', 'last_editor', 'last_edit_dates_tags', 'languages_tags', 'languages_hierarchy', 'languages_codes', 'languages', 'lang', 'labels_tags', 'labels_old', 'labels_lc', 'labels_hierarchy', 'labels', 'known_ingredients_n', 'interface_version_modified', 'interface_version_created', 'ingredients_with_unspecified_percent_sum', 'ingredients_with_unspecified_percent_n', 'ingredients_with_specified_percent_sum', 'ingredients_with_specified_percent_n', 'ingredients_that_may_be_from_palm_oil_tags', 'ingredients_that_may_be_from_palm_oil_n', 'ingredients_text_with_allergens_nl', 'ingredients_text_with_allergens', 'ingredients_text_nl_ocr_1558255948_result', 'ingredients_text_nl_ocr_1558255948', 'ingredients_text_nl', 'ingredients_text_debug', 'ingredients_tags', 'ingredients_percent_analysis', 'ingredients_original_tags', 'ingredients_n_tags', 'ingredients_n', 'ingredients_ids_debug', 'ingredients_hierarchy', 'ingredients_from_palm_oil_tags', 'ingredients_from_palm_oil_n', 'ingredients_from_or_that_may_be_from_palm_oil_n', 'ingredients_debug', 'ingredients_analysis_tags', 'ingredients_analysis', 'informers_tags', 'images', 'image_url', 'image_thumb_url', 'image_small_url', 'image_nutrition_url', 'image_nutrition_thumb_url', 'image_nutrition_small_url', 'image_ingredients_url', 'image_ingredients_thumb_url', 'image_ingredients_small_url', 'image_front_url', 'image_front_thumb_url', 'image_front_small_url', 'id', 'food_groups_tags', 'food_groups', 'entry_dates_tags', 'emb_codes_tags', 'emb_codes', 'editors_tags', 'ecoscore_tags', 'ecoscore_score', 'ecoscore_grade', 'ecoscore_data', 'data_sources_tags', 'data_sources', 'data_quality_warnings_tags', 'data_quality_tags', 'data_quality_info_tags', 'data_quality_errors_tags', 'data_quality_bugs_tags', 'creator', 'created_t', 'countries_tags', 'countries_lc', 'countries_hierarchy', 'correctors_tags', 'categories_tags', 'codes_tags', 'categories_properties_tags', 'categories_old', 'categories_hierarchy']
wanted_keys = ['nutriscore_data', 'nutriments', 'nutrient_levels', 'ingredients']
class BarcodeReader():
    def __init__(self, rec_dur, camera_id):
        self.rec_dur = rec_dur
        self.camera_id = camera_id

    # Records and tries to read barcode.
    def record(self):
        start = time.time()
        cv2.startWindowThread()
        cap = cv2.VideoCapture(self.camera_id)
        if not cap.isOpened():
            print("Cannot open camera")
            exit()

        barcode = None
        while True:
            # Capture frame-by-frame.
            succes, frame = cap.read()
            # Check is frame is read correctly.
            if not succes:
                print("Can't receive frame. Exiting ...")
                break

            # Finds barcode and reads
            if decode(frame):
                barcode = decode(frame)[0].data.decode("utf-8")
                break

            cv2.imshow('frame', frame)
            if cv2.waitKey(1) == ord('q') or time.time() - start > self.rec_dur:
                break

        cap.release()
        cv2.destroyAllWindows()
        cv2.waitKey(1)

        if barcode ==  'not found':
            return 'not found'

        # Gets food information.
        food = self.get_food(barcode)

        return food

    # Gets food item using barcode. Returns None if no information could be found.
    def get_food(self, barcode):
        search_result = openfoodfacts.products.get_product(barcode)

        if search_result['status_verbose'] == 'product not found':
            return 'not found'

        search_result = dict(search_result['product'])

        result = {}
        for key in wanted_keys:
            result[key] = search_result[key]


        return result
