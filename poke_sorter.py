import math
import tomllib


def load_config() -> tuple:
	try:
		with open("poke_sorter.toml", "rb") as f:
			data = tomllib.load(f)
			grid_x = int(data["settings"]["x"])
			grid_y = int(data["settings"]["y"])
	except:
		print("Configuration file missing or broken. Creating a new file.")
		grid_x, grid_y = update_config()
	return grid_x, grid_y


def update_config() -> tuple:
	valid_input = False
	while not valid_input:
		config_input = input(
			'Enter dimensions Horizontal by Vertical (e.g., 3x3): ')
		try:
			grid_x = int(config_input.partition("x")[0])
			grid_y = int(config_input.partition("x")[2])
			with open("poke_sorter.toml", "w") as f:
				f.write(f"[settings]\nx = {grid_x}\ny = {grid_y}")
			valid_input = True
		except ValueError:
			print("Invalid input. Please try again.")
	return grid_x, grid_y


def output(input_num: int, grid_x: int, grid_y: int) -> None:
	grid_combined = grid_x * grid_y
	row_raw = input_num / grid_combined
	slot_raw = math.ceil(row_raw)
	dex_slot = round((row_raw - math.floor(row_raw)) * grid_combined)
	if dex_slot == 0:
		dex_slot = grid_combined
	print('')
	print('Your card goes in page ', str(slot_raw), ' slot ', str(dex_slot))
	current_row = 0
	line_found = False
	while grid_y > current_row:
		current_row += 1
		print_slot = dex_slot % grid_x
		if current_row >= (dex_slot / grid_x) and line_found == False:
			if print_slot == 0:
				print('O ' * (grid_x - 1) + 'X')
			else:
				print('O ' * (print_slot - 1) + 'X ' +
					  'O ' * (grid_x - print_slot))
			line_found = True
		else:
			print('O ' * grid_x)
	print('')


def main(grid_x: int, grid_y: int) -> None:
	while True:
		print('Your current binder dimensions are:', grid_x, 'x', grid_y)
		answer = input(
			'Input Pokemon Dex number or Update to change your binder dimensions: ')
		if answer.lower() in 'update':
			grid_x, grid_y = update_config()
		try:
			output(int(answer), grid_x, grid_y)
		except ValueError:
			if not answer.lower() in 'update':
				print("That's not a valid input.")


if __name__ == "__main__":
	x, y = load_config()
	main(x, y)
