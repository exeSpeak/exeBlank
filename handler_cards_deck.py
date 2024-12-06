import random
from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum, auto

class CardType(Enum):
    ATTACK = auto()
    DEFENSE = auto()
    SKILL = auto()
    POWER = auto()

@dataclass
class Card:
    id: int
    name: str
    card_type: CardType
    energy_cost: int
    description: str
    base_damage: int = 0
    base_block: int = 0
    special_effects: Dict = None

    def __post_init__(self):
        if self.special_effects is None:
            self.special_effects = {}

class DeckManager:
    def __init__(self):
        self.draw_pile: List[Card] = []
        self.hand: List[Card] = []
        self.discard_pile: List[Card] = []
        self.exhaust_pile: List[Card] = []
        self.max_hand_size: int = 5
        self.cards_per_turn: int = 5

    def create_starter_deck(self) -> None:
        """Creates a basic starter deck with some simple cards"""
        starter_cards = [
            Card(1, "Strike", CardType.ATTACK, 1, "Deal 6 damage", base_damage=6),
            Card(2, "Strike", CardType.ATTACK, 1, "Deal 6 damage", base_damage=6),
            Card(3, "Strike", CardType.ATTACK, 1, "Deal 6 damage", base_damage=6),
            Card(4, "Defend", CardType.DEFENSE, 1, "Gain 5 block", base_block=5),
            Card(5, "Defend", CardType.DEFENSE, 1, "Gain 5 block", base_block=5),
            Card(6, "Defend", CardType.DEFENSE, 1, "Gain 5 block", base_block=5),
        ]
        self.draw_pile.extend(starter_cards)
        self.shuffle_draw_pile()

    def shuffle_draw_pile(self) -> None:
        """Shuffles the draw pile"""
        random.shuffle(self.draw_pile)

    def draw_card(self, amount: int = 1) -> List[Card]:
        """Draws specified number of cards from draw pile"""
        drawn_cards = []
        for _ in range(amount):
            if not self.draw_pile:
                self.reshuffle_discard_into_draw()
                if not self.draw_pile:  # If still empty after reshuffling
                    break
            drawn_cards.append(self.draw_pile.pop())
        return drawn_cards

    def reshuffle_discard_into_draw(self) -> None:
        """Moves all cards from discard pile to draw pile and shuffles"""
        self.draw_pile.extend(self.discard_pile)
        self.discard_pile.clear()
        self.shuffle_draw_pile()

    def start_turn(self) -> None:
        """Handles the start of a new turn"""
        cards_to_draw = min(self.cards_per_turn, self.max_hand_size - len(self.hand))
        drawn_cards = self.draw_card(cards_to_draw)
        self.hand.extend(drawn_cards)

    def end_turn(self) -> None:
        """Handles the end of a turn"""
        self.discard_pile.extend(self.hand)
        self.hand.clear()

    def play_card(self, card_index: int, target=None) -> Optional[Card]:
        """Plays a card from hand"""
        if 0 <= card_index < len(self.hand):
            card = self.hand.pop(card_index)
            self.discard_pile.append(card)
            return card
        return None

    def add_card_to_deck(self, card: Card) -> None:
        """Adds a new card to the discard pile"""
        self.discard_pile.append(card)

    def remove_card_from_deck(self, card_id: int) -> bool:
        """Permanently removes a card from the deck"""
        for pile in [self.draw_pile, self.hand, self.discard_pile]:
            for card in pile:
                if card.id == card_id:
                    pile.remove(card)
                    return True
        return False

    def exhaust_card(self, card: Card) -> None:
        """Moves a card to the exhaust pile"""
        self.exhaust_pile.append(card)

    def get_deck_size(self) -> int:
        """Returns total number of cards in deck"""
        return len(self.draw_pile) + len(self.hand) + len(self.discard_pile)

    def get_pile_sizes(self) -> Dict[str, int]:
        """Returns the size of each pile"""
        return {
            "draw": len(self.draw_pile),
            "hand": len(self.hand),
            "discard": len(self.discard_pile),
            "exhaust": len(self.exhaust_pile)
        }
