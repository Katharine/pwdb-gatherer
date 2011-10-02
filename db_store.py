#!/usr/bin/env python
import MySQLdb
import element.parser
import element.util
import element.properties

def main():
	p = element.parser.ElementParser('data/elements.data', 'data/parser.conf')
	db = MySQLdb.connect(host="mattpf.net", user="pwdb", passwd="85_CE3oAN*<ct4[pslaX", db="pwdb")
	descriptions = element.util.ElementDescriptions('data/item_ext_desc.txt')
	colours = element.util.ElementColours('data/item_color.txt')
	store_weapon_types(db, p)
	store_armor_types(db, p)
	store_addons(db, p)
	store_skills(db, p)
	store_weapons(db, p, descriptions, colours)
	store_armor(db, p, descriptions, colours)
	store_ornaments(db, p, descriptions, colours)
	store_sets(db, p)
	store_chi(db, p, descriptions, colours)
	store_materials(db, p, descriptions, colours)
	store_quest_items(db, p, descriptions, colours)
	store_recipes(db, p)
	store_tomes(db, p, descriptions, colours)
	store_remedies(db, p, descriptions, colours)
	store_apoc(db, p, descriptions, colours)
	store_smilies(db, p, descriptions, colours)
	store_spawns(dp)
	db.close()

def store_chi(db, p, d, co):
	c = db.cursor()
	for chi in p.chi_stones:
		c.execute("INSERT IGNORE INTO generic_items (id, name, icon, model, grade, stack_count, type, buy_price, sell_price, description, colour) VALUES (%s, %s, %s, %s, %s, %s, 'chi', %s, %s, %s, %s)", (
			chi.id,
			chi.name,
			chi.surfaces,
			chi.models,
			chi.grade,
			chi.stack,
			chi.price_buy,
			chi.price_sell,
			d[chi.id] if chi.id in d else None,
			co[chi.id] if chi.id in co else None))
		c.execute("""INSERT IGNORE INTO items (id, name, colour, type, icon) VALUES (%s, %s, %s, 'chi', %s)""", (chi.id, chi.name, co[chi.id] if chi.id in co else None, chi.surfaces))
	c.close()

def store_materials(db, p, d, co):
	c = db.cursor()
	for mat in p.materials:
		c.execute("INSERT IGNORE INTO generic_items (id, name, icon, model, stack_count, type, buy_price, sell_price, description, colour) VALUES (%s, %s, %s, %s, %s, 'material', %s, %s, %s, %s)", (
			mat.id,
			mat.name,
			mat.surfaces,
			mat.models,
			mat.stack,
			mat.price_buy,
			mat.price_sell,
			d[mat.id] if mat.id in d else None,
			co[mat.id] if mat.id in co else None))
		c.execute("""INSERT IGNORE INTO items (id, name, colour, type, icon) VALUES (%s, %s, %s, 'material', %s)""", (mat.id, mat.name, co[mat.id] if mat.id in co else None, mat.surfaces))
	c.close()

def store_rewards(db, p, d, co):
	c = db.cursor()
	for reward in p.quest_rewards:
		c.execute("INSERT IGNORE INTO generic_items (id, name, icon, model, stack_count, type, buy_price, sell_price, flags, description, colour) VALUES (%s, %s, %s, %s, %s, 'reward', %s, %s, %s, %s, %s)", (
			reward.id,
			reward.name,
			reward.surfaces,
			reward.models,
			reward.stack,
			reward.price_buy,
			reward.price_sell,
			reward.flags,
			d[reward.id] if reward.id in d else None,
			co[reward.id] if reward.id in co else None))
		c.execute("""INSERT IGNORE INTO items (id, name, colour, type, icon) VALUES (%s, %s, %s, 'reward', %s)""", (reward.id, reward.name, co[reward.id] if reward.id in co else None, reward.surfaces))
	c.close()

def store_quest_items(db, p, d, co):
	c = db.cursor()
	for item in p.quest_items:
		c.execute("INSERT IGNORE INTO generic_items (id, name, icon, stack_count, type, flags, description, colour) VALUES (%s, %s, %s, %s, 'quest item', %s, %s, %s)", (
			item.id,
			item.name,
			item.surfaces,
			item.stack,
			item.flags,
			d[item.id] if item.id in d else None,
			co[item.id] if item.id in co else None))
		c.execute("""INSERT IGNORE INTO items (id, name, colour, type, icon) VALUES (%s, %s, %s, 'quest item', %s)""", (item.id, item.name, co[item.id] if item.id in co else None, item.surfaces))
	c.close()

def store_weapons(db, p, d, co):
	c = db.cursor()
	for weapon in p.weapons:
		c.execute("""INSERT IGNORE INTO weapons (id, class_mask, type, subtype, name, model_right, model_left, model_dropped, icon, str, dex, mag, vit, level, grade, min_patk, max_patk, min_matk, max_matk, `range`, attack_rate, durability, max_durability, level_up_addon, material_need, sell_price, buy_price, repair_price, drop_0_socket, drop_1_socket, drop_2_socket, craft_0_socket, craft_1_socket, craft_2_socket, addons_0, addons_1, addons_2, addons_3, unique_addon, drop_min_durability, drop_max_durability, decompose_price, decompose_time, decompose_to, decompose_amount, stack_count, has_guid, proc_type, description, colour, nonrandom_addons, reputation, flags)
					VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
					weapon.id,
					weapon.class_mask,
					weapon.type,
					weapon.subtype,
					weapon.name,
					weapon.models1,
					weapon.models2,
					weapon.models3,
					weapon.surfaces,
					weapon.str_required,
					weapon.agi_required,
					weapon.int_required,
					weapon.con_required,
					weapon.level_required,
					weapon.grade,
					weapon.min_patk,
					weapon.max_patk,
					weapon.min_matk,
					weapon.max_matk,
					weapon.range,
					weapon.attack_rate,
					weapon.durability,
					weapon.max_durability,
					weapon.level_up_addon,
					weapon.material_need,
					weapon.price_sell,
					weapon.price_buy,
					weapon.price_repair,
					weapon.drop_0_socket,
					weapon.drop_1_socket,
					weapon.drop_2_socket,
					weapon.craft_0_socket,
					weapon.craft_1_socket,
					weapon.craft_2_socket,
					weapon.probability_0_addons,
					weapon.probability_1_addons,
					weapon.probability_2_addons,
					weapon.probability_3_addons,
					weapon.probability_of_unique_addons,
					weapon.drop_min_durability,
					weapon.drop_max_durability,
					weapon.decompose_price,
					weapon.decompose_time,
					weapon.decompose_to,
					weapon.decompose_amount,
					1, # weapon.stack_count, # This is producing garbage and the answer should always be one for weapons.
					weapon.has_guid,
					weapon.proc_type,
					d[weapon.id] if weapon.id in d else None,
					co[weapon.id] if weapon.id in co else None,
					int(weapon.craft_addon_id_0 == 0 and weapon.craft_probability_0 == 1),
					weapon.reputation_required,
					weapon.flags
				))
		c.execute("""INSERT IGNORE INTO items (id, name, colour, type, icon) VALUES (%s, %s, %s, %s, %s)""", (weapon.id, weapon.name, co[weapon.id] if weapon.id in co else None, 'weapon', weapon.surfaces))
		# These numbers may change.
		query = "INSERT IGNORE INTO item_addons (item, addon, probability, `type`) VALUES "
		value_part = "(%s, %s, %s, %s)"
		values = []
		# Drop addons
		for i in xrange(44, 108, 2):
			addon = weapon[i]
			prob = weapon[i+1]
			if addon != 0 and (prob != 0 or (weapon.craft_addon_id_0 == 0 and weapon.craft_probability_0 == 1)):
				values.extend((weapon.id, addon, prob, 'drop'))
		# Craft addons
		for i in xrange(108, 172, 2):
			addon = weapon[i]
			prob = weapon[i+1]
			if addon != 0 and prob != 0:
				values.extend((weapon.id, addon, prob, 'craft'))
		# Unique addons
		for i in xrange(172, 204, 2):
			addon = weapon[i]
			prob = weapon[i+1]
			if addon != 0 and prob != 0:
				values.extend((weapon.id, addon, prob, 'unique'))
		query += ', '.join([value_part for x in xrange(len(values) / 4)])
		if len(values) > 0:
			c.execute(query, values)
	c.close()

def store_armor(db, p, d, co):
	c = db.cursor()
	for armor in p.armor:
		c.execute("""INSERT IGNORE INTO armor (id, class_mask, type, subtype, name, model, icon, str, dex, mag, vit, level, grade, phys_def, metal_def, wood_def, water_def, fire_def, earth_def, mana, hp, evasion, durability, max_durability, level_up_addon, sell_price, buy_price, repair_price, drop_0_socket, drop_1_socket, drop_2_socket, drop_3_socket, drop_4_socket, craft_0_socket, craft_1_socket, craft_2_socket, craft_3_socket, craft_4_socket, addons_0, addons_1, addons_2, addons_3, drop_min_durability, drop_max_durability, decompose_price, decompose_time, decompose_to, decompose_amount, stack_count, description, colour, nonrandom_addons, reputation, flags)
					VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
					armor.id,
					armor.class_mask,
					armor.type,
					armor.subtype,
					armor.name,
					armor.models,
					armor.surfaces,
					armor.str_required,
					armor.agi_required,
					armor.int_required,
					armor.con_required,
					armor.level_required,
					armor.grade,
					armor.physical_defense,
					armor.metal_defense,
					armor.wood_defense,
					armor.water_defense,
					armor.fire_defense,
					armor.earth_defense,
					armor.mana,
					armor.hp,
					armor.dodge_rate,
					armor.durability,
					armor.max_durability,
					armor.level_up_addon,
					armor.price_sell,
					armor.price_buy,
					armor.price_repair,
					armor.drop_0_socket,
					armor.drop_1_socket,
					armor.drop_2_socket,
					armor.drop_3_socket,
					armor.drop_4_socket,
					armor.craft_0_socket,
					armor.craft_1_socket,
					armor.craft_2_socket,
					armor.craft_3_socket,
					armor.craft_4_socket,
					armor.probability_0_addons,
					armor.probability_1_addons,
					armor.probability_2_addons,
					armor.probability_3_addons,
					armor.drop_min_durability,
					armor.drop_max_durability,
					armor.decompose_price,
					armor.decompose_time,
					armor.decompose_to,
					armor.decompose_amount,
					1, # weapon.stack_count, # This is producing garbage and the answer should always be one for weapons.
					d[armor.id] if armor.id in d else None,
					co[armor.id] if armor.id in co else None,
					int(armor.craft_addon_id_0 == 0 and armor.craft_probability_0 == 1),
					armor.reputation_required,
					armor.flags
				))
		c.execute("""INSERT IGNORE INTO items (id, name, colour, type, icon) VALUES (%s, %s, %s, %s, %s)""", (armor.id, armor.name, co[armor.id] if armor.id in co else None, 'armour', armor.surfaces))
		# These numbers may change.
		query = "INSERT IGNORE INTO item_addons (item, addon, probability, `type`) VALUES "
		value_part = "(%s, %s, %s, %s)"
		values = []
		# Drop addons
		for i in xrange(56, 120, 2):
			addon = armor[i]
			prob = armor[i+1]
			if addon != 0 and (prob != 0 or (armor.craft_addon_id_0 == 0 and armor.craft_probability_0 == 1)):
				values.extend((armor.id, addon, prob, 'drop'))
		# Craft addons
		for i in xrange(120, 182, 2):
			addon = armor[i]
			prob = armor[i+1]
			if addon != 0 and prob != 0:
				values.extend((armor.id, addon, prob, 'craft'))
		query += ', '.join([value_part for x in xrange(len(values) / 4)])
		if len(values) > 0:
			c.execute(query, values)
	c.close()

def store_ornaments(db, p, d, co):
	c = db.cursor()
	for ornament in p.ornaments:
		c.execute("""INSERT INTO ornaments (id, class_mask, type, subtype, name, model, icon, str, dex, mag, vit, level, reputation, grade, phys_def, metal_def, wood_def, water_def, fire_def, earth_def, phys_atk, mag_atk, evasion, durability, max_durability, level_up_addon, sell_price, buy_price, repair_price, addons_0, addons_1, addons_2, addons_3, drop_min_durability, drop_max_durability, decompose_price, decompose_time, decompose_to, decompose_amount, stack_count, description, colour, nonrandom_addons, flags)
					VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
					ornament.id,
					ornament.class_mask,
					ornament.type,
					ornament.subtype,
					ornament.name,
					ornament.models,
					ornament.surfaces,
					ornament.str_required,
					ornament.agi_required,
					ornament.int_required,
					ornament.con_required,
					ornament.level_required,
					ornament.reputation_required,
					ornament.grade,
					ornament.physical_defense,
					ornament.metal_defense,
					ornament.wood_defense,
					ornament.water_defense,
					ornament.fire_defense,
					ornament.earth_defense,
					ornament.physical_attack,
					ornament.magic_attack,
					ornament.dodge_rate,
					ornament.durability,
					ornament.max_durability,
					ornament.level_up_addon,
					ornament.price_sell,
					ornament.price_buy,
					ornament.price_repair,
					ornament.probability_0_addons,
					ornament.probability_1_addons,
					ornament.probability_2_addons,
					ornament.probability_3_addons,
					ornament.drop_min_durability,
					ornament.drop_max_durability,
					ornament.decompose_price,
					ornament.decompose_time,
					ornament.decompose_to,
					ornament.decompose_amount,
					1, # weapon.stack_count, # This is producing garbage and the answer should always be one for weapons.
					d[ornament.id] if ornament.id in d else None,
					co[ornament.id] if ornament.id in co else None,
					int(ornament.craft_addon_id_0 == 0 and ornament.craft_probability_0 == 1),
					ornament.flags
				))
		c.execute("""INSERT  INTO items (id, name, colour, type, icon) VALUES (%s, %s, %s, %s, %s)""", (ornament.id, ornament.name, co[ornament.id] if ornament.id in co else None, 'ornament', ornament.surfaces))
		# These numbers may change.
		query = "INSERT  INTO item_addons (item, addon, probability, `type`) VALUES "
		value_part = "(%s, %s, %s, %s)"
		values = []
		# Drop addons
		for i in xrange(45, 109, 2):
			addon = ornament[i]
			prob = ornament[i+1]
			if addon != 0 and (prob != 0 or (ornament.craft_addon_id_0 == 0 and ornament.craft_probability_0 == 1)):
				values.extend((ornament.id, addon, prob, 'drop'))
		# Craft addons
		for i in xrange(109, 173, 2):
			addon = ornament[i]
			prob = ornament[i+1]
			if addon != 0 and prob != 0:
				values.extend((ornament.id, addon, prob, 'craft'))
		query += ', '.join([value_part for x in xrange(len(values) / 4)])
		if len(values) > 0:
			c.execute(query, values)
	c.close()

def store_weapon_types(db, p):
	c = db.cursor()
	for t in p.weapon_major_types:
		c.execute("INSERT IGNORE INTO weapon_types (id, name) VALUES (%s, %s)", (t.id, t.name))
	
	for t in p.weapon_sub_types:
		c.execute("INSERT IGNORE INTO weapon_subtypes (id, name, gfx, sfx, `interval`, short_range, action_type) VALUES (%s, %s, %s, %s, %s, %s, %s)", (
					t.id,
					t.name,
					t.gfx,
					t.sfx,
					t.attack_rate,
					t.attack_short_range,
					t.action_type))
	
	c.close()

def store_armor_types(db, p):
	c = db.cursor()
	for t in p.armor_major_types:
		c.execute("INSERT IGNORE INTO armor_types (id, name) VALUES (%s, %s)", (t.id, t.name))
	
	for t in p.armor_sub_types:
		c.execute("INSERT IGNORE INTO armor_subtypes (id, name, mask) VALUES (%s, %s, %s)", (t.id, t.name, t.mask))
	c.close()

def store_addons(db, p):
	c = db.cursor()
	addon_types = element.properties.ItemProperties('data/item_ext_prop.txt')
	for addon in p.equipment_addons:
		t = addon_types[addon.id] if addon.id in addon_types else None
		c.execute("INSERT IGNORE INTO addons (id, `group`, `values`, value1, value2, value3) VALUES (%s, %s, %s, %s, %s, %s)", (addon.id, t, addon.number_of_values, addon.value_1, addon.value_2, addon.value_3))
	c.close()

def store_skills(db, p):
	c = db.cursor()
	skills = element.util.ElementSkills('data/skillstr.txt')
	for skill in skills:
		skill = skills[skill]
		c.execute("INSERT IGNORE INTO skill_descriptions (id, name, description) VALUES (%s, %s, %s)", (skill.id, skill.name, skill.description))
	c.close()

def store_sets(db, p):
	c = db.cursor()
	for s in p.complect_bonus:
		c.execute("""INSERT IGNORE INTO item_sets (id, name, item_count, item_1, item_2, item_3, item_4, item_5, item_6, bonus_2, bonus_3, bonus_4, bonus_5, bonus_6, completion_effect)
					VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
					s.id,
					s.name,
					s.item_amount,
					s.item_1 if s.item_1 != 0 else None,
					s.item_2 if s.item_2 != 0 else None,
					s.item_3 if s.item_3 != 0 else None,
					s.item_4 if s.item_4 != 0 else None,
					s.item_5 if s.item_5 != 0 else None,
					s.item_6 if s.item_6 != 0 else None,
					s.property_2 if s.property_2 != 0 else None,
					s.property_3 if s.property_3 != 0 else None,
					s.property_4 if s.property_4 != 0 else None,
					s.property_5 if s.property_5 != 0 else None,
					s.property_6 if s.property_6 != 0 else None,
					s.full_set_effect))
	c.close()

def store_recipes(db, p):
	c = db.cursor()
	for recipe in p.recipes:
		c.execute("INSERT INTO recipes (id, type, subtype, name, craft_level, craft_skill, price, failure_rate, exp, spirit, quantity, upgrade_for, mysterious_float, mysterious_int) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (
					recipe.id,
					recipe.type,
					recipe.subtype,
					recipe.name,
					recipe.craft_level,
					recipe.craft_skill,
					recipe.craft_price,
					recipe.failure_rate,
					recipe.exp,
					recipe.sp,
					recipe.amount_produced,
					recipe.upgrading_item if recipe.upgrading_item != 0 else None,
					recipe.mysterious_float,
					recipe.mysterious_int))
		for i in xrange(8, 16, 2):
			item = recipe[i]
			probability = recipe[i+1]
			if item != 0:
				c.execute("INSERT INTO recipe_output (recipe, item, probability) VALUES (%s, %s, %s)", (recipe.id, item, probability))
		query = "INSERT INTO recipe_input (recipe, item, quantity) VALUES "
		value_part = "(%s, %s, %s)"
		values = []
		for i in xrange(22, 58, 2):
			item = recipe[i]
			quantity = recipe[i+1]
			if item !=0 and quantity != 0:
				values.extend((recipe.id, item, quantity))
		if recipe.upgrading_item:
			values.extend((recipe.id, recipe.upgrading_item, 1))
		query += ', '.join(value_part for x in xrange(len(values) / 3))
		if len(values) > 0:
			c.execute(query, values)
	c.close()

def store_tomes(db, p, d, co):
	c = db.cursor()
	for tome in p.heaven_books:
		c.execute("""INSERT IGNORE INTO tomes (
					id, name, model, icon, buy_price, sell_price, decompose_to, decompose_amount,
					decompose_price, decompose_time, flags, description, colour) VALUES (
					%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
						tome.id,
						tome.name,
						tome.models,
						tome.surfaces,
						tome.price_buy,
						tome.price_sell,
						tome.decompose_to,
						tome.decompose_amount,
						tome.decompose_price,
						tome.decompose_time,
						tome.flags,
						d[tome.id] if tome.id in d else None,
						co[tome.id] if tome.id in co else None,
					))
		
		c.execute("""INSERT  INTO items (id, name, colour, type, icon) VALUES (%s, %s, %s, %s, %s)""", (tome.id, tome.name, co[tome.id] if tome.id in co else None, 'tome', tome.surfaces))

		# These numbers may change.
		query = "INSERT IGNORE INTO item_addons (item, addon, probability, `type`) VALUES "
		value_part = "(%s, %%s, 1.0, 'craft')" % tome.id
		values = []
		# Drop addons
		for i in xrange(4, 14):
			addon = tome[i]
			if addon != 0:
				values.append(addon)
		query += ', '.join(value_part for x in xrange(len(values)))
		if len(values) > 0:
			c.execute(query, values)
	c.close()

def store_remedies(db, p, d, co):
	c = db.cursor()
	for remedy in p.remedies:
		c.execute("""INSERT IGNORE INTO remedies (
					id, name, colour, description, type, subtype, model, icon, level, cooldown, hp, mp,
					recovery_time, sell_price, buy_price, stack_count, flags) VALUES (
					%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
						remedy.id,
						remedy.name,
						co[remedy.id] if remedy.id in co else None,
						d[remedy.id] if remedy.id in d else None,
						remedy.type,
						remedy.subtype,
						remedy.models,
						remedy.surfaces,
						remedy.level_required,
						remedy.cooldown / 1000.0,
						remedy.hp,
						remedy.mp,
						max(remedy.hp_time, remedy.mp_time),
						remedy.price_sell,
						remedy.price_buy,
						remedy.stack,
						remedy.flags))
		c.execute("""INSERT INTO items (id, name, colour, type, icon) VALUES (%s, %s, %s, %s, %s)""", (remedy.id, remedy.name, co[remedy.id] if remedy.id in co else None, 'remedy', remedy.surfaces))
	c.close()

def store_apoc(db, p, d, co):
	c = db.cursor()
	for apoc in p.potions:
		c.execute("INSERT IGNORE INTO generic_items (id, name, icon, model, stack_count, type, buy_price, sell_price, description, colour, flags) VALUES (%s, %s, %s, %s, %s, 'apothecary', %s, %s, %s, %s, %s)", (
			apoc.id,
			apoc.name,
			apoc.surfaces,
			apoc.models,
			apoc.stack,
			apoc.price_buy,
			apoc.price_sell,
			d[apoc.id] if apoc.id in d else None,
			co[apoc.id] if apoc.id in co else None,
			apoc.flags))
		c.execute("""INSERT IGNORE INTO items (id, name, colour, type, icon) VALUES (%s, %s, %s, 'apothecary', %s)""", (apoc.id, apoc.name, co[apoc.id] if apoc.id in co else None, apoc.surfaces))
	c.close()

def store_smilies(db, p, d, co):
	c = db.cursor()
	for smiley in p.chat_speakers:
		c.execute("INSERT IGNORE INTO generic_items (id, name, icon, model, stack_count, type, buy_price, sell_price, description, colour, flags) VALUES (%s, %s, %s, %s, %s, 'smilies', %s, %s, %s, %s, %s)", (
			smiley.id,
			smiley.name,
			smiley.surfaces,
			smiley.models,
			smiley.stack,
			smiley.price_buy,
			smiley.price_sell,
			d[smiley.id] if smiley.id in d else None,
			co[smiley.id] if smiley.id in co else None,
			smiley.flags))
		c.execute("""INSERT IGNORE INTO items (id, name, colour, type, icon) VALUES (%s, %s, %s, 'smilies', %s)""", (smiley.id, smiley.name, co[smiley.id] if smiley.id in co else None, smiley.surfaces))
	c.close()

def store_mobs(db, p):
	c = db.cursor()
	for mob in p.monsters:
		e = mob.element
		plus = e.find('+')
		minus = e.find('-')
		if plus >= 0:
			strong = e[plus+1:plus+3]
		else:
			strong = None
		if minus >= 0:
			weak = e[minus+1:minus+3]
		else:
			weak = None
		# These things have WAY TOO MANY fields. D:<
		c.execute("""INSERT INTO mobs (id, type, name, strong_element, weak_element, model, gfx, 
					level, egg, hp, phys_def, metal_def, wood_def, water_def, fire_def, earth_def, 
					exp, spirit, coins_mean, coins_variance, accuracy, evasion, min_patk, max_patk, 
					`range`, `interval`, `min_matk`, `max_matk`, aggressive, aggro_range, aggro_time, 
					walk_speed, run_speed, swim_speed, drop_0_items, drop_1_items, drop_2_items, 
					drop_3_items, drop_multiplier) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
					%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
					%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
					mob.id, mob.type, mob.name, strong, weak, mob.ecm, mob.gfx, mob.level,
					mob.tameable_pet_egg, mob.hp, mob.physical_def, mob.metal_def, mob.wood_def,
					mob.water_def, mob.fire_def, mob.earth_def, mob.exp, mob.sp, mob.money_mean,
					mob.money_variance, mob.accuracy, mob.evasion, mob.min_patk, mob.max_patk,
					mob.range, mob.interval, mob.min_matk, mob.max_matk, mob.aggressive, mob.aggro_range,
					mob.aggro_time, mob.walk_speed, mob.run_speed, mob.swim_speed, mob.drop_rate_0_items,
					mob.drop_rate_1_items, mob.drop_rate_2_items, mob.drop_rate_3_items,
					mob.drop_replication_count))

		query = "INSERT INTO mob_drops (mob, item, rate) VALUES "
		value_part = "(%s, %s, %s)"
		values = []
		for i in xrange(191, 258, 2):
			drop = mob[i]
			rate = mob[i+1]
			if drop != 0 and rate != 0:
				values.extend((mob.id, drop, rate))
		query += ', '.join(value_part for x in xrange(len(values) / 3))
		if len(values) > 0:
			c.execute(query, values)
	c.close()

def store_spawns(db):
	c = db.cursor()
	spawns = element.util.SpawnLocations('data/coord_data.txt')
	for spawn_id in spawns:
		query = "INSERT INTO spawn_points (spawn, map, x, y, z) VALUES "
		value_part = "(%s, %s, %s, %s, %s)"
		values = []
		# Drop addons
		for spawn in spawns[spawn_id]:
			values.extend((spawn_id, spawn.map[:3], spawn.x, spawn.y, spawn.z))
		query += ', '.join(value_part for x in xrange(len(values) / 5))
		c.execute(query, values)

def store_shards(db, p, d, co):
	c = db.cursor()
	for shard in p.soulgems:
		colour = co[shard.id] if shard.id in co else None
		desc = d[shard.id] if shard.id in d else None
		c.execute("""INSERT INTO shards (id, type, name, icon, grade, sell_price, buy_price,
					imbue_price, purge_price, weapon_addon, armour_addon, weapon_string, 
					armour_string, flags, colour, description, stack_count) VALUES 
					(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
					shard.id,
					shard.type,
					shard.name,
					shard.surfaces,
					shard.grade,
					shard.sell_price,
					shard.buy_price,
					shard.imbue_cost,
					shard.purge_cost,
					shard.weapon_property,
					shard.armor_property,
					shard.weapon_string,
					shard.armor_string,
					shard.flags,
					colour,
					desc,
					shard.stack_count))
		c.execute("INSERT INTO items (id, name, colour, type, icon) VALUES (%s, %s, %s, %s, %s)", (
					shard.id,
					shard.name,
					colour,
					'shard',
					shard.surfaces))
	c.close()

def store_resources(db, p):
	c = db.cursor()
	for resource in p.resources:
		# Insert the resource
		c.execute("""INSERT INTO resources (id, type, name, grade, level, tool, min_time,
				max_time, exp, spirit, model, q1, q1_prob, q2, q2_prob, quest, uninterruptible,
				permanent) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
				%s, %s)""", (
				resource.id,
				resource.type,
				resource.name,
				resource.grade,
				resource.level,
				resource.tool,
				resource.min_time,
				resource.max_time,
				resource.experience,
				resource.spirit,
				resource.models,
				resource.quantity_1,
				resource.quantity_1_probability,
				resource.quantity_2,
				resource.quantity_2_probability,
				resource.quest_required,
				resource.uninterruptible,
				resource.permanent
				))
		
		# Insert the items
		query = "INSERT INTO resource_items (resource, item, probability) VALUES "
		value_part = "(%s, %s, %s)"
		values = []
		for i in xrange(12, 44, 2):
			item = resource[i]
			rate = resource[i+1]
			if item != 0 and rate != 0:
				values.extend((resource.id, item, rate))
		query += ', '.join(value_part for x in xrange(len(values) / 3))
		if len(values) > 0:
			c.execute(query, values)

		# Insert the mobs
		query = "INSERT INTO resource_mobs (resource, mob, quantity, distance) VALUES "
		value_part = "(%s, %s, %s, %s)"
		values = []
		for i in xrange(51, 63, 3):
			mob = resource[i]
			quantity = resource[i+1]
			distance = resource[i+2]
			if mob != 0 and quantity != 0:
				values.extend((resource.id, mob, quantity, distance))
		query += ', '.join(value_part for x in xrange(len(values) / 4))
		if len(values) > 0:
			c.execute(query, values)
	c.close()

if __name__ == '__main__':
	main()
